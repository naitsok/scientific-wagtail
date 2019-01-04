
from functools import partial

from django import template
from django.conf import settings

import bleach
from markdownmath.utils import markdownify


register = template.Library()


@register.filter()
def markdown(value):
    return markdownify(value)