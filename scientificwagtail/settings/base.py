"""
Django settings for scientificwagtail project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'users',
    'main',
    'search',
    'sciwagblocks',

    'wagtail.contrib.forms',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.redirects',
    'wagtail.contrib.routable_page',
    'wagtail.contrib.table_block',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',
    'el_pagination',
    'markdownx',
    'wagtailmenus',
    'captcha',
    'widget_tweaks',
    'hitcount',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.forms',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    # 'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

    'main.middleware.DjangoAdminAccessMiddleware',
    'sciwagblocks.middleware.MarkdownxAccessMiddleware',
]

ROOT_URLCONF = 'scientificwagtail.urls'
import django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
            os.path.join(BASE_DIR, 'main', 'templates', 'main'),
            os.path.join(BASE_DIR, 'users', 'templates', 'users'),
            os.path.join(BASE_DIR, 'markdownmath', 'templates', 'markdownmath'),
            os.path.join(BASE_DIR, 'sciwagblocks', 'templates', 'sciwagblocks'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtailmenus.context_processors.wagtailmenus',
                'main.context_processors.archive',
                'main.context_processors.root_page',
                'main.context_processors.recent_posts',
            ],
        },
    },
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting' 

WSGI_APPLICATION = 'scientificwagtail.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/2.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Custom user

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
   'users.backends.EmailLoginBackend',
)

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'


# tags settings

TAGGIT_CASE_INSENSITIVE = True

# multiword tags
TAG_SPACES_ALLOWED = True


# El-pagination settings

EL_PAGINATION_PAGE_LIST_CALLABLE = 'el_pagination.utils.get_page_numbers' # get_page_number get_elastic_page_numbers

EL_PAGINATION_PER_PAGE = 5

EL_PAGINATION_PREVIOUS_LABEL = '<i class="fas fa-arrow-left"></i> Previous'

EL_PAGINATION_NEXT_LABEL = 'Next <i class="fas fa-arrow-right"></i>'


# Wagtail menus settings

WAGTAILMENUS_ACTIVE_ANCESTOR_CLASS = 'active'


# django-simple-captcha settings

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'

CAPTCHA_IMAGE_SIZE = (120, 60)

CAPTCHA_FONT_SIZE = 30


# hitcount settings
# after this time the hit from the same user will be counted again
HITCOUNT_KEEP_HIT_ACTIVE  = {'days' : 30 }
# time to keep hits in database - now the hits are stored indefinitely
# HITCOUNT_KEEP_HIT_IN_DATABASE = {'days': 30}


# MarkdownX settings

MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.tables',
    'markdown.extensions.abbr',
    'markdown.extensions.attr_list',
    'markdown.extensions.codehilite',
    'markdown.extensions.sane_lists',
    'markdown.extensions.toc',
    'sciwagblocks.extensions.mathjax',
]

MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {
    'markdown.extensions.codehilite': {
        'css_class': 'highlight',
        },
}

MARKDOWNX_MARKDOWNIFY_FUNCTION = 'sciwagblocks.utils.markdownify'


# Project settings

# markdownmath app settings

MARKDOWNX_WHITELIST_TAGS = [
  'a',
  'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
  'abbr',
  'acronym',
  'b',
  'blockquote',
  'em',
  'i',
  'li',
  'ol',
  'p',
  'strong',
  'ul',
  'table',
  'thead',
  'tbody',
  'tr',
  'th',
  'td',
  'span',
  'pre',
  'sub',
  'sup',
  'code',
  'div',
  'br',
]

MARKDOWNX_WHITELIST_ATTRS = [
    'href',
    'src',
    'alt',
    'class',
    'title',
    'style',
]

MARKDOWNX_WHITELIST_STYLES = [
    'color',
    'font-weight',
    'font-size',
]

MARKDOWNX_WHITELIST_PROTOCOLS = ['http', 'https', 'mailto']

# Linkify links appeared in text
MARKDOWNX_LINKIFY_TEXT = True

# Linkify emails
MARKDOWNX_LINKIFY_PARSE_EMAIL = True

# callbacks to modify your links
MARKDOWNX_LINKIFY_CALLBACKS = None

# do not linify content inside of these tags
MARKDOWNX_LINKIFY_SKIP_TAGS = ['pre', 'code',]

# if True - strip tags, if False - escape tags
MARKDOWNX_STRIP = True

# if False - not bleaching
MARKDOWNX_BLEACH = True


# Wagtail settings

WAGTAIL_APPEND_SLASH = True

WAGTAIL_SITE_NAME = 'Scientific Wagtail'

# Search backed for development
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.db',
    }
}

# Disable password reset since it is personal site and the user is created using command line
WAGTAIL_PASSWORD_RESET_ENABLED = False

# Passwords can be changed
WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = True

# Users do have passwords to log in
WAGTAILUSERS_PASSWORD_ENABLED = True

# Users must have paswords
WAGTAILUSERS_PASSWORD_REQUIRED = True

# See also embeds configuration at https://docs.wagtail.io/en/v2.11.3/advanced_topics/embeds.html#configuring-embed-finders
WAGTAILEMBEDS_RESPONSIVE_HTML = True

# Custom admin login form based on email
WAGTAILADMIN_USER_LOGIN_FORM = 'users.forms.EmailLoginForm'

# Changes whether the Submit for Moderation button is displayed in the action menu
WAGTAIL_MODERATION_ENABLED = True

# To count usage of images and documents
WAGTAIL_USAGE_COUNT_ENABLED = True

# Date and time formats for admin
WAGTAIL_DATE_FORMAT = '%d.%m.%Y.'
WAGTAIL_DATETIME_FORMAT = '%d.%m.%Y. %H:%M'
WAGTAIL_TIME_FORMAT = '%H:%M'

# Static files to prevent chaching and outdate
WAGTAILADMIN_STATIC_FILE_VERSION_STRINGS = True

# Text editor
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6',
             'bold', 'italic', 'ol', 'ul', 'hr',
             'link', 'document-link', 'image', 'embed',
             'code', 'superscript', 'subscript', 'strikethrough']
        }
    }
}


# main app settings

# base urls for urls.py
WAGTAIL_ADMIN_BASE_URL = 'admin/'

WAGTAIL_DOCUMENTS_BASE_URL = 'documents/'

DJANGO_ADMIN_BASE_URL = 'django-admin/'

MARKDOWNX_BASE_URL = 'markdownx/'

CAPTCHA_BASE_URL = 'captcha/'


# Tag cloud settings

POST_TAG_CLOUD_MIN_WEIGHT = 1.5

POST_TAG_CLOUD_MAX_WEIGHT = 2.0

# number of tags to show in cloud
# will sort by number and then select and order by name
# if -1 - selects all tags
TAG_CLOUD_TAG_LIMIT = -1

# number of recent posts
RECENT_POSTS_LENGTH = 5

# Archive settings

# number of archive dates to display before the rest of the list is hidden
DISPLAY_ARCHIVE_LENGTH = 5

# Disqus settings
DISQUS_URL = 'https://example.disqus.com/embed.js'

