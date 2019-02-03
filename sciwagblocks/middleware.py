from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
from django.conf import settings


MARKDOWNX_URLS_PATH = getattr(settings, 'MARKDOWNX_URLS_PATH', 'markdownx/markdownify')


class MarkdownxAccessMiddleware:
    """
    Middleware that provides access for markdown to HTML path. 
    The access is always allowed for logged in users.
    Others are redirected to 404 page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if MARKDOWNX_URLS_PATH in request.path.lower() and not request.user.is_authenticated:
            # not authenticated users are not allowed to
            # access django admin
            raise Http404

        return self.get_response(request)