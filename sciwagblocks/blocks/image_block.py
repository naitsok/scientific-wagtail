from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from .markdownx_block import MarkdownxBlock


class CaptionedImageBlock(blocks.StructBlock):
    """Block that contains additional caption field for image."""
    image = ImageChooserBlock()
    caption = MarkdownxBlock(required=False)

    class Meta:
        template = 'image_block/captioned_image.html'
        icon = 'image'