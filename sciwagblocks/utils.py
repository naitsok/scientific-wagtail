# based on django-markdownify
# https://github.com/erwinmatijsen/django-markdownify
# https://django-markdownify.readthedocs.io/en/latest/settings.html

from functools import partial

from django import template
from django.conf import settings

import bleach
from markdownx.utils import markdownify as markdownx_markdownify


def markdownify(value):
    # Get the settings or set defaults if not set

    # Bleach settings
    whitelist_tags = getattr(settings, 'MARKDOWNX_WHITELIST_TAGS', bleach.sanitizer.ALLOWED_TAGS)
    whitelist_attrs = getattr(settings, 'MARKDOWNX_WHITELIST_ATTRS', bleach.sanitizer.ALLOWED_ATTRIBUTES)
    whitelist_styles = getattr(settings, 'MARKDOWNX_WHITELIST_STYLES', bleach.sanitizer.ALLOWED_STYLES)
    whitelist_protocols = getattr(settings, 'MARKDOWNX_WHITELIST_PROTOCOLS', bleach.sanitizer.ALLOWED_PROTOCOLS)

    # Markdown settings
    strip = getattr(settings, 'MARKDOWNX_STRIP', True)

    # Bleach Linkify
    linkify = None
    linkify_text = getattr(settings, 'MARKDOWNX_LINKIFY_TEXT', True)

    if linkify_text:
        linkify_parse_email = getattr(settings, 'MARKDOWNX_LINKIFY_PARSE_EMAIL', False)
        linkify_callbacks = getattr(settings, 'MARKDOWNX_LINKIFY_CALLBACKS', None)
        linkify_skip_tags = getattr(settings, 'MARKDOWNX_LINKIFY_SKIP_TAGS', None)
        linkifyfilter = bleach.linkifier.LinkifyFilter

        linkify = [partial(linkifyfilter,
                callbacks=linkify_callbacks,
                skip_tags=linkify_skip_tags,
                parse_email=linkify_parse_email
                )]

    # Convert markdown to html
    html = markdownx_markdownify(value) #.replace('&amp;', '&')
    # Sanitize html if wanted
    if getattr(settings, 'MARKDOWNX_BLEACH', True):

        cleaner = bleach.Cleaner(tags=whitelist_tags,
                                 attributes=whitelist_attrs,
                                 styles=whitelist_styles,
                                 protocols=whitelist_protocols,
                                 strip=strip,
                                 filters=linkify,
                                 )

        html = cleaner.clean(html)
    return html