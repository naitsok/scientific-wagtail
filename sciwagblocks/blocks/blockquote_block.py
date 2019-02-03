from django.utils.translation import ugettext_lazy as _

from wagtail.core import blocks


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
        template = 'blockquote_block/blockquote.html'