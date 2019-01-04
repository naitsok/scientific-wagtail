from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, Http404
from django.conf import settings


DJANGO_ADMIN_BASE_URL = getattr(settings, 'DJANGO_ADMIN_BASE_URL', r'^django-admin/').lower().replace(r'^', '').replace(r'/', '')


class DjangoAdminAccessMiddleware:
    """
    Middleware that provides access for django admin part of the
    website. The access is allowed for users, who first logged into Wagtail admin.
    Others are redirected to 404 page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if DJANGO_ADMIN_BASE_URL in request.path.lower() and not request.user.is_authenticated:
            # not authenticated users are not allowed to
            # access django admin
            raise Http404

        return self.get_response(request)