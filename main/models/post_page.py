from django import forms
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import Tag, TaggedItemBase
# from taggit.managers import TaggableManager

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (FieldPanel, StreamFieldPanel,
    MultiFieldPanel, FieldRowPanel, InlinePanel)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from hitcount.models import HitCountMixin, HitCount
from hitcount.views import HitCountMixin as ViewHitCountMixin

from main.edit_handlers import ReadOnlyPanel
from sciwagblocks.blocks import (
    CaptionedTableBlock, 
    CaptionedEquationBlock,
    TwoColumnBlock,
    CaptionedImageBlock,
    CustomBlockquoteBlock,
    MarkdownxBlock,
)


class PostPage(Page, HitCountMixin):
    """Page for posts, the main content of the website."""

    # Database fields

    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        )
    body = StreamField([
        ('cut', blocks.CharBlock(
                classname='full subtitle',
                help_text='After this block the post will be cutted when displayed on the home page. On the post page this field is ignored.'
            )
        ),
        ('paragraph', blocks.RichTextBlock()),
        ('quote', CustomBlockquoteBlock(classname='full')),
        ('figure', CaptionedImageBlock(label='Figure')),
        ('embed', EmbedBlock()),
        ('document', DocumentChooserBlock(help_text='All the text in other blocks, which is the same as document title will be replaced with the link to the document.')),
        ('markdown', MarkdownxBlock()),
        ('equation', CaptionedEquationBlock()),
        ('pages', blocks.PageChooserBlock()),
        ('columns', TwoColumnBlock()),
        ('table', CaptionedTableBlock()),
        ('table_figure', CaptionedImageBlock(label='Table as Figure', icon='table')),
        ])
    pin_on_home = models.BooleanField(
        default=False,
        help_text=_('Indicates if the Post is pinned on the Home page.'),
        verbose_name=_('Pin on Home page')
        )
    show_sidebar = models.BooleanField(
        default=True,
        help_text=_('Indicates if the sidebar with contents, figures and equations is shown on the page.'),
        verbose_name=_('Show sidebar')
    )
    show_comments = models.BooleanField(
        default=True,
        help_text=_('Indicates if comments are shown on the page.'),
        verbose_name=_('Show comments')
    )
    generate_figure_numbers = models.BooleanField(
        default=False,
        help_text=_('Indcates if figure numbers (such as Figure 1) should be generated for Figure block when rendring post.'),
        verbose_name=_('Generate figure numbers')
    )
    generate_table_numbers = models.BooleanField(
        default = False,
        help_text=_('Indicates if  table numbers (such as Table 1) should be geberated for Table block when rendering post.'),
        verbose_name=_('Generate table numbers')
    )
    generate_equation_numbers = models.BooleanField(
        default=False,
        help_text=_('Indicates if equation numbers (such as (1)) should be added on the right side of the Equation block when rendering post.'),
        verbose_name=_('Generate equation numbers')
    )
    categories = ParentalManyToManyField(
        'main.BlogCategory',
        verbose_name=_('Categories'),
        blank=True,
    )
    tags = ClusterTaggableManager(
        through='main.PostTag',
        help_text=None,
        blank=True
    )
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field='pk',
        related_query_name='hit_count_relation',
    )

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('body', partial_match=True, boost=4),
        index.FilterField('pin_on_home'),
        index.FilterField('categories'),
        index.FilterField('tags')
        ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
        ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('header_image'),
        FieldPanel('tags'),
        InlinePanel('blog_categories', label=_('Categories'))
        ]

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel('pin_on_home'),
                FieldPanel('show_sidebar'),
                FieldPanel('show_comments'),
                FieldPanel('generate_figure_numbers'),
                FieldPanel('generate_table_numbers'),
                FieldPanel('generate_equation_numbers')
            ],
            heading=_('Post settings')
        ),
        MultiFieldPanel(
            [
                ReadOnlyPanel('first_published_at', heading='First published at'),
                ReadOnlyPanel('last_published_at', heading='Last published at'),
                ReadOnlyPanel('hit_counts', heading='Number of views')
            ],
            heading=_('General information')
        ),
    ]

    # Parent page / subpage type rules
    # PostPage can have children PostPages. In this case the parent page is
    # considered as 'series' type post and the links to the children pages are
    # generated, when page is accessed. Also the links to parent page and siblings
    # are rendered on the child page.
    
    parent_page_types = ['main.HomePage', 'main.PostPage']
    subpage_types = ['main.PostPage']


    # Methods

    def update_body(self):
        """Updates captions of figures, tables and equations if PostPage settings require so.
        Collects figures and tables into a separate list to ease the rendering of Graphics
        sidebar on the PostPage. Collects equations into another separate list to ease the 
        rendering of Equations sidebar on the PostPage."""
        fig_idx = 1
        tbl_idx = 1
        eq_idx = 1
        graphics = list()
        equations = list()
        for block in self.body:
            if block.block_type == 'figure':
                if self.generate_figure_numbers:
                    block.value['caption'] = _('<b>Figure ') + str(fig_idx) + '.</b> ' + block.value['caption']
                    fig_idx += 1
                graphics.append(block)
            if block.block_type == 'table' or block.block_type == 'table_figure':
                if self.generate_table_numbers:
                    block.value['caption'] = _('<b>Table ') + str(tbl_idx) + '.</b> ' + block.value['caption']
                    tbl_idx += 1
                graphics.append(block)
            if block.block_type == 'equation':
                if self.generate_equation_numbers:
                    block.value['caption'] = _('<b>Equation ') + str(eq_idx) + '.</b> ' + block.value['caption']
                    eq_idx += 1
                equations.append(block)
            if block.block_type == 'columns':
                for column in [block.value['left'], block.value['right']]:
                    for col_block in column:
                        if col_block.block_type == 'figure':
                            if self.generate_figure_numbers:
                                col_block.value['caption'] = _('<b>Figure ') + str(fig_idx) + '.</b> ' + col_block.value['caption']
                                fig_idx += 1
                            graphics.append(col_block)
                        if col_block.block_type == 'table' or col_block.block_type == 'table_figure':
                            if self.generate_table_numbers:
                                col_block.value['caption'] = _('<b>Table ') + str(tbl_idx) + '.</b> ' + col_block.value['caption']
                                tbl_idx += 1
                            graphics.append(col_block)
                        if col_block.block_type == 'equation':
                            if self.generate_equation_numbers:
                                col_block.value['caption'] = _('<b>Equation ') + str(eq_idx) + '.</b> ' + col_block.value['caption']
                                eq_idx += 1
                            equations.append(col_block)
        return graphics, equations

    

    def is_series(self):
        """Verifies that post is series"""
        # parent_page = self.get_parent().specific
        if self.get_parent().specific_class == PostPage:
            # this is the child post of series
            return True
        if self.get_descendant_count() > 0:
            # this is parent post of series
            return True
        return False
        

    def get_context(self, request, *args, **kwargs):

        graphics, equations = self.update_body()
        context =  super().get_context(request, *args, **kwargs)
        context['post'] = self
        context['graphics'] = graphics
        context['equations'] = equations
        context['previous_post'] = PostPage.objects.live().filter(
            first_published_at__lt=self.first_published_at
        ).order_by('-first_published_at').first()
        context['next_post'] = PostPage.objects.live().filter(
            first_published_at__gt=self.first_published_at
        ).order_by('first_published_at').first()

        context['is_series'] = False
        # verify post is series
        parent_page = self.get_parent().specific
        if parent_page.specific_class == PostPage:
            # this is a child post from the series
            context['is_series'] = True
            context['parent_post'] = parent_page
            context['child_posts'] = parent_page.get_descendants().live()
        else:
            # this is a normal post, check if it is series
            if self.get_descendant_count() > 0:
                # this post is the parent post for series
                context['is_series'] = True
                context['parent_post'] = self
                context['child_posts'] = self.get_descendants().live()

        return context

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


class PostTag(TaggedItemBase):
    content_object = ParentalKey(
        'main.PostPage',
        on_delete=models.CASCADE,
        related_name='tagged_items'
        )


@register_snippet
class BlogCategory(models.Model):
    """Blog categories for posts."""

    # Database fields

    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(unique=True, max_length=255, blank=False)

    # Editor panels configuration

    panels = [
        FieldPanel('name', classname='full'),
        FieldPanel('slug', classname='full')
        ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class PostPageBlogCategory(models.Model):
    """A connection class for inline panel to work."""
    post_page = ParentalKey(
        'main.PostPage', 
        on_delete=models.CASCADE,
        related_name='blog_categories', 
    )
    blog_category = models.ForeignKey(
        'main.BlogCategory', 
        on_delete=models.CASCADE, 
        related_name='post_pages'
    )

    panels = [
        SnippetChooserPanel('blog_category'),
    ]

    class Meta:
        unique_together = ('post_page', 'blog_category')


@register_snippet
class TagProxy(Tag):
    """Proxy for tags for Wagtail admin."""
    class Meta:
        proxy = True
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


