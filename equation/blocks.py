from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.forms import Widget, CharField
from wagtail.core.blocks import FieldBlock


class EquationWidget(Widget):
    template_name = 'equation/widget.html'
    class Media:
        js = [
            'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js',
            'equation/js/equation.js',
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


class EquationBlock(FieldBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = CharField(required=required, help_text=help_text, widget=EquationWidget())
        super(EquationBlock, self).__init__(**kwargs)

    def value_from_form(self, value):
        return value

    class Meta:
        icon = 'cog'

    
