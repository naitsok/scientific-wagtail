from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.forms import Widget, CharField

from wagtail.core import blocks

from .markdownx_block import MarkdownxBlock


class EquationWidget(Widget):
    template_name = 'equation_block/widget.html'
    class Media:
        js = [
            'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js',
            'sciwagblocks/equation_block/js/equation.js',
        ]

    def get_context(self, name, value, attrs):
        context = {}
        context['widget'] = {
            'name': name,
            'is_hidden': self.is_hidden,
            'required': self.is_required,
            'value': value,
            'attrs': self.build_attrs(attrs),
            'template_name': self.template_name,
        }
        return context


    def render(self, name, value, attrs=None):
        # id gets set, but I dont know where.
        # We need it removed so the JS will work correctly
        # attrs.pop('id')
        context = self.get_context(name, value, attrs)
        return mark_safe(render_to_string(self.template_name, context))


class EquationBlock(blocks.FieldBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = CharField(required=required, help_text=help_text, widget=EquationWidget())
        super(EquationBlock, self).__init__(**kwargs)

    def value_from_form(self, value):
        return value

    class Meta:
        template = 'equation_block/equation.html'
        icon = 'cog'

    
class CaptionedEquationBlock(blocks.StructBlock):
    """Block that contains equation block and markdownmath block for caption.
    The caption is displayed only when the equation is opened in modal.
    The caption never appears in main text of post."""
    equation = EquationBlock()
    caption = MarkdownxBlock(required=False)

    class Meta:
        template = 'equation_block/captioned_equation.html'
        icon = 'cogs'
