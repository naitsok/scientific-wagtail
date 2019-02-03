# Custom blocks for StreamField

from django import forms
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from wagtail.core import blocks
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

from markdownmath.blocks import MarkdownxBlock

from equation.blocks import EquationBlock


class CustomBlockquoteBlock(blocks.StructBlock):
    """Custom blockquote block with the quote text and 
    the optional quote author and source."""
    quote = blocks.TextBlock(
        required=True,
        help_text=_('Quote text.'),
        rows=3
    )
    author = blocks.CharBlock(
        required=False,
        help_text=_('Author of the quoted text.')
    )
    source = blocks.CharBlock(
        required=False,
        help_text=_('Source of the quoted text.')
    )

    class Meta:
        icon = 'openquote'
        template = 'main/components/custom_blockquote_block.html'


class CaptionedImageBlock(blocks.StructBlock):
    """Block that contains additional caption field for image."""
    image = ImageChooserBlock()
    caption = MarkdownxBlock(required=False)

    class Meta:
        icon = 'image'


class CaptionedEquationBlock(blocks.StructBlock):
    """Block that contains equation block and markdownmath block for caption.
    The caption is displayed only when the equation is opened in modal.
    The caption never appears in main text of post."""
    equation = EquationBlock()
    caption = MarkdownxBlock(required=False)

    class Meta:
        icon = 'cogs'


class ColumnBlock(blocks.StreamBlock):
    """Block to put content into one column.
    Standalone equations are not included in the column.
    Although equation are possible in markdown field."""
    paragraph = blocks.RichTextBlock()
    image = CaptionedImageBlock()
    markdown = MarkdownxBlock()
    pages = blocks.PageChooserBlock()

    
class TwoColumnBlock(blocks.StructBlock):
    left = ColumnBlock(icon='arrow-left', label='Left column content')
    right = ColumnBlock(icon='arrow-right', label='Right column content')

    class Meta:
        template = 'main/components/two_column_block.html'
        icon = 'grip'
        label = 'Two Columns'


from wagtail.contrib.table_block.blocks import TableBlock


class TableColWidthBlock(TableBlock):
    """Table Block, where you can set column width.
    """
    pass