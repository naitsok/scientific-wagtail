from django import template


register = template.Library()


@register.filter
def index(lst, idx):
    return lst[idx]