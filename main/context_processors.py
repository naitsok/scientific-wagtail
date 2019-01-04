from django.conf import settings

from .models import PostPage


DISPLAY_ARCHIVE_LENGTH = getattr(settings, 'DISPLAY_ARCHIVE_LENGTH', 5)
RECENT_POSTS_LENGTH = getattr(settings, 'RECENT_POSTS_LENGTH', 5)


def archive(request):
    """Returns list of distict months + years to generate archive links."""
    archive =  list(PostPage.objects.live().dates('first_published_at', 'month', order='DESC'))
    return { 
        'archive_displayed': archive[:DISPLAY_ARCHIVE_LENGTH],
        'archive_hidden': archive[DISPLAY_ARCHIVE_LENGTH:],
    }


def root_page(request):
    """Returns the root page instance. Needed for url generations."""
    return { 
        'root_page': request.site.root_page.specific,
    }


def recent_posts(request):
    """Gets recent posts to display on footer."""
    return {
        'recent_posts': PostPage.objects.live().order_by('-first_published_at')[:RECENT_POSTS_LENGTH],
    }