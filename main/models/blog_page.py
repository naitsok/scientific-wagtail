from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.search import index

from wagtailmenus.models import MenuPageMixin
from wagtailmenus.panels import menupage_panel

from hitcount.models import HitCountMixin, HitCount
from hitcount.views import HitCountMixin as ViewHitCountMixin

from sciwagblocks.blocks import (
    TwoColumnBlock, 
    CaptionedImageBlock,
    CustomBlockquoteBlock,
    MarkdownxBlock,
    CaptionedTableBlock,
)
from main.edit_handlers import ReadOnlyPanel


class BlogPage(Page, MenuPageMixin, HitCountMixin):
    """A Generic blog page to contain a content, such as
    About, Publications, Research
    """

    # Common fields

    show_in_menus_default = True

    # Database fields

    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Image, that appears right after the title.')
        )
    body = StreamField([
        # ('heading', blocks.CharBlock(classname='full subtitle')),
        ('paragraph', blocks.RichTextBlock()),
        ('quote', CustomBlockquoteBlock(classname='full')),
        ('image', CaptionedImageBlock()),
        ('embed', EmbedBlock()),
        ('markdown', MarkdownxBlock()),
        ('columns', TwoColumnBlock()),
        ('pages', blocks.PageChooserBlock()),
        ('document', DocumentChooserBlock()),
        ('table', CaptionedTableBlock()),
        ])
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
        object_id_field='pk',
        related_query_name='hit_count_relation',
    )

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('body', partial_match=True, boost=2)
        ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
        ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('header_image'),
        ]

    settings_panels = Page.settings_panels + [
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

    # Parent page / subpage type rules
    
    parent_page_types = ['main.HomePage', 'main.BlogPage']
    subpage_types = ['main.BlogPage', 'main.FormPage']

    # Methods

    def hit_counts(self):
        if self.pk is not None:
            # the page is created and hitcounts make sense
            return self.hit_count.hits
        else:
            return 0

    def serve(self, request, *args, **kwargs):
        hit_count = HitCount.objects.get_for_object(self)
        ViewHitCountMixin.hit_count(request, hit_count)
        return super().serve(request, *args, **kwargs)
