import datetime
from datetime import date

from django.db import models
from django.db.models import Count
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.search import index
from wagtail.search.models import Query

from hitcount.models import HitCountMixin, HitCount
from hitcount.views import HitCountMixin as ViewHitCountMixin

from .post_page import PostPage, PostTag, TagProxy, BlogCategory
from main.edit_handlers import ReadOnlyPanel


class HomePage(RoutablePageMixin, Page, HitCountMixin):
    """Home Page - the entry point to the Blog, will list all published posts,
    name, website icon. Parent page for Blog Page, Blog Post and Form Page.
    """

    # Instance fields

    pinned_posts = []
    posts = []
    search_header = None
    search_term = ''

    # Database fields
    navbar_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Image, that appears in navbar.'),
        verbose_name='Brand image',
    )
    slogan = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Phrase, that appears in navbar on the right to the brand image.'),
        verbose_name=_('Slogan'),
    )
    title_in_navbar = models.BooleanField(
        default=True,
        help_text=_('Indicates, if title of the page is showing in navbar.'),
        verbose_name=_('Show home page title in navbar'),
    )
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field='pk',
        related_query_name='hit_count_relation',
    )

    # Search index configuration

    search_fields = [] 

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('title_in_navbar'),
        FieldPanel('slogan'),
        ImageChooserPanel('navbar_image'),
    ]

    promote_panels = Page.promote_panels

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                ReadOnlyPanel('first_published_at', heading='First published at'),
                ReadOnlyPanel('last_published_at', heading='Last published at'),
                ReadOnlyPanel('hit_counts', heading='Number of views'),
            ],
            heading=_('General information')
        )
    ]

    # Parent page / subpage type rules
    
    parent_page_types = []
    subpage_types = ['main.BlogPage', 'main.PostPage', 'main.FormPage']

    # Methods

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)
        context['pinned_posts'] = self.pinned_posts
        context['posts'] = self.posts
        context['page'] = self
        context['search_header'] = self.search_header
        if not self.search_term.endswith('.'):
            self.search_term = self.search_term + '.'
        context['search_term'] = self.search_term
        posts_per_page = getattr(settings, 'EL_PAGINATION_PER_PAGE', 5)
        context['posts_per_page'] = posts_per_page

        return context

    def get_all_live_posts(self):
        """Gets all posts (PostPages). Sorts by first published date."""
        return PostPage.objects.live()

    def count_pinned_posts(self):
        """Counts the posts (PostPages), if there are some to be pinned on Home"""
        return self.get_all_live_posts().filter(pin_on_home=True).count()

    def get_pinned_posts(self):
        """Returns posts (PostPages) that are pinned on Home.
        Pinned posts are sorted by the last published date."""
        return self.get_all_live_posts().filter(pin_on_home=True).order_by('-last_published_at')

    def get_unpinned_posts(self):
        """Returns normal (unpinned) posts (PostPages).
        Normal posts are sorted by the first published date."""
        return self.get_all_live_posts().filter(pin_on_home=False).order_by('-first_published_at')

    def hit_counts(self):
        if self.pk is not None:
            # the page is created and hitcounts make sense
            return self.hit_count.hits
        else:
            return 0

    def serve(self, request, *args, **kwargs):
        hit_count = HitCount.objects.get_for_object(self)
        ViewHitCountMixin.hit_count(request, hit_count)
        return super().serve(request, *args, **kwargs)

    # Home Page Routing

    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(jan?|feb?|mar?|apr?|may?|jun?|jul?|aug?|sep?|oct?|nov?|dec?)/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    @route(r'^(\d{4})/(jan?|feb?|mar?|apr?|may?|jun?|jul?|aug?|sep?|oct?|nov?|dec?)/(\d{2})/$')
    def posts_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        """The PostPages are listed by date. No pinned posts after date select."""
        self.posts = self.get_all_live_posts().filter(first_published_at__year=year)
        self.search_header = _('Filtered by appeared at:')
        self.search_term = year
        if month:
            try:
                month = datetime.datetime.strptime(month, '%b').month
            except ValueError:
                month = int(month)
                
            self.posts = self.posts.filter(first_published_at__month=month)
            try:
                df = DateFormat(date(int(year), int(month), 1))
            except ValueError:
                # the year, or month or date is wrong, return 404
                raise Http404(_('Wrong date.'))
            self.search_term = df.format('F Y')

        if day:
            self.posts = self.posts.filter(first_published_at__day=day)
            self.search_term = date_format(date(int(year), int(month), int(day)))

        self.posts = self.posts.order_by('-first_published_at')
        return self.serve(request, *args, **kwargs)

    @route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
    @route(r'^(\d{4})/(jan?|feb?|mar?|apr?|may?|jun?|jul?|aug?|sep?|oct?|nov?|dec?)/(\d{2})/(.+)/$')
    def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
        """Returns PostPage (one post) with date added to the url in addition to
        the slug."""
        post_page = self.get_all_live_posts().filter(slug=slug).first()
        if not post_page:
            raise Http404
        return post_page.serve(request, *args, **kwargs)

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def posts_by_tag(self, request, tag, *args, **kwargs):
        """The PostPages are listed by tag. No pinned posts after tag select."""
        self.posts = self.get_all_live_posts().filter(tags__slug=tag).order_by('-first_published_at')
        self.search_header = _('Filtered by tag:')
        self.search_term = TagProxy.objects.get(slug=tag).name

        return self.serve(request, *args, **kwargs)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def posts_by_category(self, request, category, *args, **kwargs):
        """The PostPages are listed by tag. No pinned posts after tag select."""
        self.posts = self.get_all_live_posts().filter(blog_categories__blog_category__slug=category).order_by('-first_published_at')
        self.search_header = _('Posts in category:')
        self.search_term = BlogCategory.objects.get(slug=category).name

        return self.serve(request, *args, **kwargs)

    @route(r'^by/(?P<username>[-_\w\@\+\.]+)/$')
    def posts_by_owner(self, request, username, *args, **kwargs):
        """The posts listed by owner username."""
        self.posts = self.get_all_live_posts().filter(owner__username=username).order_by('-first_published_at')
        self.search_header = _('Posts published by:')
        self.search_term = username

        return self.serve(request, *args, **kwargs)

    @route(r'^search/$')
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        if search_query:
            self.posts = self.get_all_live_posts().search(search_query)
            self.search_header = _('Search results for:')
            self.search_term = search_query

            # Log the query so Wagtail can suggest promoted results
            Query.get(search_query).add_hit()
        
        return self.serve(request, *args, **kwargs)

    @route(r'^$')
    def home(self, request, *args, **kwargs):
        """The default page returned when the website is accessed."""
        self.pinned_posts = self.get_pinned_posts()
        self.posts = self.get_unpinned_posts()

        return self.serve(request, *args, **kwargs)