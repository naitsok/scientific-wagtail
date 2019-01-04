from django import forms
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from markdownx.fields import MarkdownxFormField

from wagtail.core import blocks


class MarkdownxBlock(blocks.FieldBlock):
    """The block for markdownx field."""

    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = MarkdownxFormField(
            required=required,
            help_text=help_text
        )
        super().__init__(**kwargs)

    def id_for_label(self, prefix):
        return self.field.widget.id_for_label(prefix)

    def render_form(self, value, prefix='', errors=None):
        """Replace the original render_form of FieldBlock to
        render my streamfield widget for markdown, that incorporates
        script to initialize the markdownx.
        """
        field = self.field
        widget = field.widget

        widget_attrs = {'id': prefix, 'placeholder': self.label}

        field_value = field.prepare_value(self.value_for_form(value))

        if hasattr(widget, 'render_with_errors'):
            widget_html = widget.render_with_errors(prefix, field_value, attrs=widget_attrs, errors=errors)
            widget_has_rendered_errors = True
        else:
            widget_html = widget.render(prefix, field_value, attrs=widget_attrs)
            widget_has_rendered_errors = False

        return render_to_string('markdownmath_widget.html', {
            'name': self.name,
            'classes': self.meta.classname,
            'prefix': prefix,
            'widget': widget_html,
            'field': field,
            'errors': errors if (not widget_has_rendered_errors) else None
        })

    class Meta:
        # No icon specified here, because that depends on the purpose that the
        # block is being used for. Feel encouraged to specify an icon in your
        # descendant block type
        icon = "code"
        default = None