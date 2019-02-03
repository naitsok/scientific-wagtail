
from wagtail.core import blocks

from .markdownx_block import MarkdownxBlock
from .image_block import CaptionedImageBlock

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
        template = 'column_block/two_column_block.html'
        icon = 'grip'
        label = 'Two Columns'