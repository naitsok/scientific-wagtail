# django-taggit-templatetags2 does not work correctly with ParentalKey
# and ClusterTaggableManager. In particular, the tag cloud fails to calculate
# the number of PostPages per PostTag. That's why a custom tepmlate tag is
# created here to make a tag cloud for PostPages.

from operator import itemgetter

from django import template
from django.conf import settings
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

import six

from main.models import PostTag
from main.models import BlogCategory


MIN_WEIGHT =  getattr(settings, 'POST_TAG_CLOUD_MIN_WEIGHT', 1.0)
MAX_WEIGHT = getattr(settings, 'POST_TAG_CLOUD_MAX_WEIGHT', 6.0)
TAG_LIMIT = getattr(settings, 'TAG_CLOUD_TAG_LIMIT', -1)


register = template.Library()

def get_tag_weight_func(tag_count_min, 
                        tag_count_max, 
                        weight_min=MIN_WEIGHT, 
                        weight_max=MAX_WEIGHT):

    def f(tag_count, 
          tag_count_min=tag_count_min,
          tag_count_max=tag_count_max,
          weight_min=weight_min,
          weight_max=weight_max):
        """Calculates weight of tag with number of counts tag_count, corresponding min 
        and max values obtained from database and desired weigh_min and weight_max values.
        """
        if tag_count_min == tag_count_max:
            factor = 1.0
        else:
            factor = float(weight_max - weight_min) / float(tag_count_max-tag_count_min)

        tag_weight = weight_min + (tag_count - tag_count_min) * factor

        return tag_weight

    return f


@register.inclusion_tag('main/components/tag_cloud.html', takes_context=True)
def render_tag_cloud(context, home_page):
    """Creates tag cloud. home_page is needed to correctly generate the link to
    HomePage, that will list the posts, which contain the tag.
    """
    queryset = PostTag.objects.values('tag__name', 'tag__slug', 'tag__pk').annotate(count=Count('tag__pk'))

    if queryset:
        if TAG_LIMIT > 0:
            # queryset can be ordered only before evaluation and slice evaluates the query
            # to order after slicing, sorted function is called
            queryset = queryset.order_by('-count')[:TAG_LIMIT]
            counts = queryset.values_list('count', flat=True)
            weight_func = get_tag_weight_func(min(counts), max(counts))
            queryset = sorted(queryset, key=itemgetter('tag__name'))
        else:
            # get all tags, order them by name and get min and max values 
            # for calculatio of font weight
            counts = queryset.values_list('count', flat=True)
            weight_func = get_tag_weight_func(min(counts), max(counts))
            queryset = queryset.order_by('tag__name')

        # calculate weights for the displayed tags
        for tag in queryset:
            tag['weight'] = weight_func(tag['count'])
    
    context.update({
        'tags': queryset, 
        'home_page': home_page.specific,
        'num_tags': len(queryset),
        'max_font_size': MAX_WEIGHT
    })

    return context


@register.inclusion_tag('main/components/blog_categories.html', takes_context=True)
def render_blog_categories(context, home_page):
    """Renders categories to be displayed in the sidebar.
    home_page is needed for url generation. Also counts
    number of posts per category."""
    context.update({
        'categories': BlogCategory.objects.annotate(num_posts=Count('post_pages')).order_by('name'),
    })
    return context


@register.simple_tag()
def post_date_url(post, root_page):
    """Generates post url that includes the first_published_at date."""
    date = post.first_published_at
    url = root_page.url + root_page.specific.reverse_subpage(
        'post_by_date_slug',
        args=(
            date.year,
            date.strftime('%b').lower(),
            date.strftime('%d'),
            post.slug
        )     
    )
    return url


@register.inclusion_tag('main/components/post.html', takes_context=True)
def render_post(context, post, is_in_list):
    """Renders one post with categoties, tags and urls. root_page is 
    needed to correctly generate the urls. It is not specified here
    since it is available from context processor. The context must be flattened
    in order to correctly pass through the block of body (StreamField):
    https://github.com/wagtail/wagtail/issues/3045.
    is_in_list indicates id the title should be a link to the post page.
    Needed when post rendered from list of posts."""

    flat_context = context.flatten()
    flat_context['post'] = post
    flat_context['categories'] = post.blog_categories.all()
    flat_context['tags'] = post.tags.all()
    flat_context['is_in_list'] = is_in_list
    return flat_context


@register.inclusion_tag('main/components/comments/disqus.html', takes_context=True)
def render_comments(context, post_page, root_page):
    """Renders disqus comments for the specified post page."""
    path = post_date_url(post_page, root_page)

    raw_url = context['request'].get_raw_uri()
    parse_result = six.moves.urllib.parse.urlparse(raw_url)
    abs_path = six.moves.urllib.parse.urlunparse([
        parse_result.scheme,
        parse_result.netloc,
        path,
        '',
        '',
        ''
    ])

    context.update(
        {
            'disqus_page_url': abs_path,
            'disqus_identifier': post_page.first_published_at.strftime('%Y-%b-%d').lower() + '-' + post_page.slug,
            'disqus_url': getattr(settings, 'DISQUS_URL', 'https://example.disqus.com/embed.js'),
        }
    )
    return context


@register.simple_tag
def increment_idx(idx):
    """Increments value of idx by 1. 
    Needs when image and equation numbers are generated."""
    return idx + 1


@register.simple_tag
def swap_bool(value):
    return not value


@register.simple_tag(takes_context=True)
def set_context_var(context, key, value):
    """Sets global variable, that can be used in e.g. 
    nested loops in templates."""
    context.dicts[0][key] = value
    return ''


@register.simple_tag(takes_context=True)
def get_context_var(context, key):
    return context.dicts[0][key]


@register.simple_tag(takes_context=True)
def increment_context_var(context, key):
    # context[key] = int(context[key]) + 1
    context.dicts[0][key] = context.dicts[0][key] + 1
    return ''


@register.simple_tag
def create_list(*args):
    return list(args)