from django import template

from sciwagblocks.utils import markdownify


register = template.Library()


@register.filter
def index(lst, idx):
    return lst[idx]


@register.filter()
def markdown(value):
    return markdownify(value)