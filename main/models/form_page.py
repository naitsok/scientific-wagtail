from django import forms
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core import mail
from django.utils.translation import ugettext, ugettext_lazy as _

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.admin.utils import send_mail
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import (
    AbstractEmailForm, AbstractFormField, FORM_FIELD_CHOICES
)
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtailmenus.models import MenuPageMixin
from wagtailmenus.panels import menupage_panel

from captcha.fields import CaptchaField
from captcha.models import CaptchaStore

from hitcount.models import HitCountMixin, HitCount
from hitcount.views import HitCountMixin as ViewHitCountMixin

from main.edit_handlers import ReadOnlyPanel


class CaptchaFormBuilder(FormBuilder):
    CAPTCHA_FIELD_NAME = 'captcha'

    @property
    def formfields(self):
        # Add wagtailcaptcha to formfields property
        fields = super().formfields
        fields[self.CAPTCHA_FIELD_NAME] = CaptchaField()

        return fields


def remove_captcha_field(form):
    form.fields.pop(CaptchaFormBuilder.CAPTCHA_FIELD_NAME, None)
    form.cleaned_data.pop(CaptchaFormBuilder.CAPTCHA_FIELD_NAME, None)


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm, MenuPageMixin, HitCountMixin):

    form_builder = CaptchaFormBuilder

    # Common fields

    show_in_menus_default = True

    # Database fields

    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    body = RichTextField(
        blank=True,
        verbose_name=_('Body'),
        help_text=_('Text before the form.')
    )
    send_email_to_visitor = models.BooleanField(
        default=True,
        verbose_name=_('Send email to visitor'),
        help_text=_('Indicates if email should be sent to the visitor, who submitted the form (in case of EmailField is in form).')
    )
    visitor_email_subject = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Visitor email subject'),
        help_text=_('Subject of the email to be sent to the visitor, who submitted the form.')
    )
    visitor_email_body = models.TextField(
        blank=True,
        verbose_name=_('Visitor email text'),
        help_text=_('Text of the email to be sent to the visitor, who submitted the form.')
    )
    thank_you_text = RichTextField(
        blank=True,
        verbose_name=_('Text after form submission'),
        help_text=_('Text, that appears after form submission.')
    )
    show_search = models.BooleanField(
        default=True,
        verbose_name=_('Show search on sidebar'),
        help_text=_('Adds search form to the page sidebar.')
    )
    show_tag_cloud = models.BooleanField(
        default=True,
        verbose_name=_('Show tag cloud'),
        help_text=_('Adds tag cloud to the page sidebar.')
    )
    show_categories = models.BooleanField(
        default=True,
        verbose_name=_('Show categories'),
        help_text=_('Adds categories to the page sidebar.')
    )
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation',
    )

    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('body', classname="full"),
        FieldPanel('thank_you_text', classname='full'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], 'Admin email settings'),
        MultiFieldPanel([
            FieldPanel('send_email_to_visitor'),
            FieldPanel('visitor_email_subject'),
            FieldPanel('visitor_email_body', widget=forms.Textarea()),
        ], 'Visitor email settings'),
        InlinePanel('form_fields', label='Form fields'),
    ]

    settings_panels = AbstractEmailForm.settings_panels + [
        menupage_panel,
        MultiFieldPanel(
            [
                FieldPanel('show_search'),
                FieldPanel('show_tag_cloud'),
                FieldPanel('show_categories'),
            ],
            heading=_('Page settings')
        ),
        MultiFieldPanel(
            [
                ReadOnlyPanel('first_published_at', heading='First published at'),
                ReadOnlyPanel('last_published_at', heading='Last published at'),
                ReadOnlyPanel('hit_counts', heading='Number of views'),
            ],
            heading=_('General information')
        ),
    ]

    parent_page_types = ['main.HomePage', 'main.BlogPage']
    subpage_types = []

    def process_form_submission(self, form):
        remove_captcha_field(form)
        return super(FormPage, self).process_form_submission(form)

    def hit_counts(self):
        if self.pk is not None:
            # the page is created and hitcounts make sense
            return self.hit_count.hits
        else:
            return 0

    def send_mail(self, form):
        """Slightly modified version of the default send_mail
        from Wagtail's AbstractEmailForm. It will send confirmation 
        email to the contacting person if there is an EmailField found
        in the form."""
        # the addresses added when the form page was created in admin.
        to_addresses_form_page = [x.strip() for x in self.to_address.split(',')]
        # check from_address
        from_address = 'webmaster@localhost'
        if self.from_address:
            from_address = self.from_address
        elif hasattr(settings, 'DEFAULT_FROM_EMAIL'):
            from_address = settings.DEFAULT_FROM_EMAIL
        # address entered in the form by the visitor, will be filled if EmailField is found
        to_address_visitor = None
        content = []

        for field in form:
            # get email if the field is of correct type
            if isinstance(field.field, forms.fields.EmailField):
                to_address_visitor = field.value().replace('\n', '').replace('\r', '')
            # combine all values
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            content.append('{}: {}'.format(field.label, value))
        content = '\n'.join(content)

        # send email to the 
        site_name = getattr(settings, 'WAGTAIL_SITE_NAME', 'Wagtail-Scientific')
        if self.send_email_to_visitor and to_address_visitor is not None:
            email_visitor = mail.EmailMessage(
                subject=self.visitor_email_subject,
                from_email=from_address,
                to=[to_address_visitor,],
                body=self.visitor_email_body + ugettext('\n\nYour message:\n\n') + content
            )
            email_visitor.send(fail_silently=True)

        # send email to the address, idicated when form page was created
        email_staff = mail.EmailMessage(
            subject=self.subject,
            from_email=from_address,
            to=to_addresses_form_page,
            body=content
        )
        email_staff.send(fail_silently=True)
        # send_mail(self.subject, content, addresses, self.from_address,)

    def serve(self, request, *args, **kwargs):
        hit_count = HitCount.objects.get_for_object(self)
        ViewHitCountMixin.hit_count(request, hit_count)
        return super().serve(request, *args, **kwargs)