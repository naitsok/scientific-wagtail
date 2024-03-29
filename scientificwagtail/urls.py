from django.conf import settings
from django.urls import include, re_path, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views


DJANGO_ADMIN_BASE_URL =  getattr(settings, 'DJANGO_ADMIN_BASE_URL', 'django-admin/')
WAGTAIL_ADMIN_BASE_URL =  getattr(settings, 'WAGTAIL_ADMIN_BASE_URL', 'admin/')
WAGTAIL_DOCUMENTS_BASE_URL =  getattr(settings, 'WAGTAIL_DOCUMENTS_BASE_URL', 'documents/')
MARKDOWNX_BASE_URL =  getattr(settings, 'MARKDOWNX_BASE_URL', 'markdownx/')
CAPTCHA_BASE_URL = getattr(settings, 'CAPTCHA_BASE_URL', 'captcha/')


urlpatterns = [
    path(DJANGO_ADMIN_BASE_URL, admin.site.urls),
    path(WAGTAIL_ADMIN_BASE_URL, include(wagtailadmin_urls)),
    path(WAGTAIL_DOCUMENTS_BASE_URL, include(wagtaildocs_urls)),

    # url(r'^search/$', search_views.search, name='search'),
    # according to django-markdownx docs
    path(MARKDOWNX_BASE_URL, include('markdownx.urls')),

    # according to django-simple-captcha docs
    path(CAPTCHA_BASE_URL, include('captcha.urls')),

    path('sitemap.xml', sitemap),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    re_path(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
