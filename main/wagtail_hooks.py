from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.rich_text.converters.editor_html import WhitelistRule
from wagtail.admin.rich_text.converters.html_to_contentstate import (BlockElementHandler, 
    ListElementHandler, ListItemElementHandler, InlineStyleElementHandler)
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
from wagtail.core import hooks
from wagtail.core.whitelist import allow_without_attributes, attribute_rule

from .models import (
    BlogPage, PostPage, BlogCategory, TagProxy, FormPage
)



# Register admin.css file for the wagtail admin.
@hooks.register('insert_global_admin_css', order=2)
def global_admin_css():
    """Add /static/css/admin.css."""
    return format_html('<link rel="stylesheet" href="{}">', static('css/admin.css'))


# Customizing admin menus
class BlogPageModelAdmin(ModelAdmin):
    model = BlogPage
    menu_label = _('Blog pages')
    menu_icon = 'doc-empty-inverse'
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('title', 'last_published_at', 'content_type', 'live')
    # list_filter = ('last_published_at', 'content_type', 'live')
    search_fields = ('title',)
    
    def get_extra_class_names_for_field_col(self, obj, field_name):
        if field_name == 'title':
            return ['list-title']
        return []

modeladmin_register(BlogPageModelAdmin)


class PostPageModelAdmin(ModelAdmin):
    model = PostPage
    menu_label = _('Posts')
    menu_icon = 'doc-empty'
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('title', 'last_published_at', 'content_type', 'live')
    # list_filter = ('last_published_at', 'content_type', 'live')
    search_fields = ('title',)

    def get_extra_class_names_for_field_col(self, obj, field_name):
        if field_name == 'title':
            return ['list-title']
        return []

modeladmin_register(PostPageModelAdmin)


class BlogCategoryModelAdmin(ModelAdmin):
    model = BlogCategory
    menu_label = _('Categories')
    menu_icon = 'list-ul'
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', )
    # list_filter = ('last_published_at', 'content_type', 'live')
    search_fields = ('name', )

    def get_extra_class_names_for_field_col(self, obj, field_name):
        if field_name == 'name':
            return ['list-title']
        return []

modeladmin_register(BlogCategoryModelAdmin)

class FormPageModelAdmin(ModelAdmin):
    model = FormPage
    menu_label = _('Form pages')
    menu_icon = 'form'
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('title', )
    # list_filter = ('last_published_at', 'content_type', 'live')
    search_fields = ('title', )

    def get_extra_class_names_for_field_col(self, obj, field_name):
        if field_name == 'title':
            return ['list-title']
        return []

modeladmin_register(FormPageModelAdmin)


# Make Draftail (or, precisely, draftjs_exporter) add css classes to the generated HTML
"""
@hooks.register('register_rich_text_features', order=1)
def add_classes_to_default_features(features):
    # Adds CSS classes to the default feature to be used with Bootstrap.
    # Order should be equal to 1 in @hooks.register to ensure that this hook
    # runs after wagtail.core hooks.

    features.register_converter_rule('contentstate', 'ul', {
        'from_database_format': {
            'ul': ListElementHandler('unordered-list-item'),
            'li': ListItemElementHandler(),
        },
        'to_database_format': {
            'block_map': {'unordered-list-item': {'element': 'li', 'wrapper': 'ul', 'wrapper_props': {'class': 'ul-class'}}}
        }
    })
    

    features.register_converter_rule('contentstate', 'ol', {
        'from_database_format': {
            'ol': ListElementHandler('ordered-list-item'),
            'li': ListItemElementHandler(),
        },
        'to_database_format': {
            'block_map': {'ordered-list-item': {'element': 'li', 'wrapper': 'ol', 'wrapper_props': {'class': 'ol-class'}}}
        }
    })

    features.register_converter_rule('contentstate', 'p', {
        'from_database_format': { 'p': InlineStyleElementHandler('paragraph') },
        'to_database_format': {
            'block_map': {'paragraph': {'element': 'p', 'props': {'class': 'text-justify'}}}
        }
    })
"""