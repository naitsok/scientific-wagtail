import json

from django import forms
from django.template.loader import render_to_string

from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock

from .markdownx_block import MarkdownxBlock


DEFAULT_TABLE_OPTIONS = {
    'minSpareRows': 0,
    'startRows': 3,
    'startCols': 3,
    'colHeaders': False,
    'rowHeaders': False,
    'contextMenu': [
        'row_above',
        'row_below',
        '---------',
        'col_left',
        'col_right',
        '---------',
        'alignment',
        '---------',
        'remove_row',
        'remove_col',
        '---------',
        'undo',
        'redo'
    ],
    'editor': 'text',
    'stretchH': 'all',
    'height': 108,
    'renderer': 'text',
    'autoColumnSize': False,
}


# CSS classes for alignment in the table cells
# that map the classes of the Handsontable
LEFT = 'htLeft'
CENTER = 'htCenter'
RIGHT = 'htRight'
JUSTIFY = 'htJustify'
TOP = 'htTop'
MIDDLE = 'htMiddle'
BOTTOM = 'htBottom'
DEFAULT_ALIGN_CLASSES = {
    LEFT: 'text-left',
    CENTER: 'text-center',
    RIGHT: 'text-right',
    JUSTIFY: 'text-justify',
    TOP: 'align-top',
    MIDDLE: 'align-middle',
    BOTTOM: 'align-bottom',
}


class ColWidthTableBlock(TableBlock):
    """A modified Table Block, where you can set column width.
    The integer values for column widths are added in the first row of
    the table in the editor. Then the values are summed and the 
    width percentage is calulated. See the render method.
    """

    def __init__(
        self, 
        required=True, 
        help_text=None, 
        table_options=DEFAULT_TABLE_OPTIONS, 
        align_classes=DEFAULT_ALIGN_CLASSES,
        **kwargs
        ):
        # these variables are needed when the table is rendered in the CaptionedTable StructBlock
        # the variables are filled in the value_from_form method
        self.align_classes = align_classes
        super().__init__(
            required=required, 
            help_text=help_text, 
            table_options=table_options, 
            **kwargs
        )

    @classmethod
    def parse_value(cls, value, align_classes=DEFAULT_ALIGN_CLASSES):
        """Parses the loaded data. Gets, column widths and table header. 
        Class method to by used in CaptionedTable class as well. 
        """
        if value:
            data = value.get('data', None)
            if data:

                # first deal with column widths
                col_widths = None
                first_row_is_column_width = value.get('first_row_is_column_width', False)      
                subtract_row_idx = 0 # there is a need to subtract a value from the row index for the cell alignment if the first row is used for col widths
                if first_row_is_column_width and len(data) > 0:
                    # calculate the widths of the columns. Try to convert data to int, 
                    # then sum them to obtain value for 100% width and then calculate
                    # the percentages of width.
                    subtract_row_idx = 1
                    col_widths = data[0]
                    total_width = 0.
                    conversion_error = False
                    for i, width in enumerate(col_widths):
                        try:
                            total_width = total_width + int(width)
                            col_widths[i] = int(width)
                        except ValueError:
                            conversion_error = True
                    
                    if conversion_error:
                        # if error - skip colums widths
                        col_widths = None
                    else:
                        # calculate column widths in percents
                        col_widths = list([width / total_width * 100. for width in col_widths])
                    # skip the col widths row
                    data = data[1:]

                # get the alignment
                align_data = value.get('cell_alignment', [])
                # setup all the cells to be aligned left
                cell_alignment = [[align_classes[LEFT]] * len(data[0]) for i in range(len(data))]
                if align_data:
                    for cell_align in align_data:
                        try:
                            hot_classes = cell_align['className'].strip().split()
                        except KeyError:
                            continue
                        try:
                            cell_alignment[cell_align['row'] - subtract_row_idx][cell_align['col']] = ' '.join([align_classes[hot_class] for hot_class in hot_classes])
                        except (TypeError, IndexError):
                            continue


                # deal with header row (table header)
                table_header = data[0] if len(data) > 0 and value.get('first_data_row_is_table_header', False) else None

                # get the real table data
                data = data[1:] if table_header else data

                return {
                    'col_widths': col_widths,
                    'table_header': table_header,
                    'first_col_is_header': value.get('first_col_is_header', False),
                    'data': data,
                    'header_cell_alignment': cell_alignment[0] if table_header else None,
                    'cell_alignment': cell_alignment[1:] if table_header else cell_alignment,
                }
        return None

    @property
    def media(self):
        return forms.Media(
            css = {'all': ['sciwagblocks/table_block/css/vendor/handsontable.full.min.css']},
            js = [
                'sciwagblocks/table_block/js/vendor/handsontable.full.min.js',
                'sciwagblocks/table_block/js/vendor/en-US.min.js', 
                'sciwagblocks/table_block/js/table.js',
                ]
            )

    def render(self, value, context=None):
        template = getattr(self.meta, 'template', None)
        if template and value:
            parsed_value = self.parse_value(value, align_classes=self.align_classes)

            if context is None:
                new_context = {}
            else:
                new_context = dict(context)

            new_context.update({
                'self': value,
                self.TEMPLATE_VAR: value,
                'html_renderer': self.is_html_renderer(),
            })
            new_context.update(parsed_value)
            return render_to_string(template, new_context)
        else:
            return self.render_basic(value, context=context)


class CaptionedTableBlock(blocks.StructBlock):
    """A table with column widths block plus markdowncaption block.
    """
    table = ColWidthTableBlock(table_options=DEFAULT_TABLE_OPTIONS, align_classes=DEFAULT_ALIGN_CLASSES)
    caption = MarkdownxBlock(required=False)

    def __init__(self, local_blocks=None, table_options=DEFAULT_TABLE_OPTIONS, align_classes=DEFAULT_ALIGN_CLASSES, **kwargs):
        self.declared_blocks['table'].table_options = DEFAULT_TABLE_OPTIONS
        self.declared_blocks['table'].align_classes = DEFAULT_ALIGN_CLASSES
        super().__init__(local_blocks=local_blocks, **kwargs)

    def render(self, value, context=None):
        template = getattr(self.meta, 'template', None)

        if template:
            parsed_table_value = ColWidthTableBlock.parse_value(value['table'], align_classes=self.child_blocks['table'].align_classes)
            if context is None:
                new_context = {}
            else:
                new_context = dict(context)

            new_context.update({
                'self': value,
                self.TEMPLATE_VAR: value,
            })
            new_context.update(parsed_table_value)
            return render_to_string(template, context=new_context)
        else:
            return self.render_basic(value, context=context)

    class Meta:
        template = 'table_block/blocks/captioned_table.html'
        icon = 'table'
        label = 'Table'
    