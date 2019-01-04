from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.core.fields import RichTextField
from wagtail.images.models import Image, AbstractImage, AbstractRendition

from markdownx.fields import MarkdownxFormField
from markdownx.models import MarkdownxField


class CaptionedImage(AbstractImage):
    """Image with caption."""

    caption = MarkdownxField(
        blank=True,
        verbose_name=_('Caption'),
        help_text=_('Add image caption.')
    )
    """
    caption = models.TextField(
        blank=True,
        verbose_name=_('Caption'),
        help_text=_('Add image caption.')
    )
    """

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        'caption',
    )


class CaptionedRendition(AbstractRendition):
    image = models.ForeignKey(CaptionedImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
