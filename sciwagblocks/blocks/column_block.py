
from wagtail.core import blocks

from .markdownx_block import MarkdownxBlock
from .image_block import CaptionedImageBlock
from .equation_block import CaptionedEquationBlock
from .table_block import CaptionedTableBlock

class ColumnBlock(blocks.StreamBlock):
    """Block to put content into one column.
    Standalone equations are not included in the column.
    Although equation are possible in markdown field."""
    paragraph = blocks.RichTextBlock()
    figure = CaptionedImageBlock()
    markdown = MarkdownxBlock()
    pages = blocks.PageChooserBlock()
    equation = CaptionedEquationBlock()
    table = CaptionedTableBlock()
    table_figure = CaptionedImageBlock(icon='table', label='Table as Figure')

    
class TwoColumnBlock(blocks.StructBlock):
    left = ColumnBlock(icon='arrow-left', label='Left column content')
    right = ColumnBlock(icon='arrow-right', label='Right column content')

    class Meta:
        template = 'column_block/two_column_block.html'
        icon = 'grip'
        label = 'Two Columns'