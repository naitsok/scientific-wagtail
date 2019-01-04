# Integrates django-markdownx as a StreamField block.
# To be used in Wagtail admin.
# Also renders math equations from the markdown field using MathJax.


from django.apps import AppConfig


class MarkdownMathConfig(AppConfig):
    name = 'markdownmath'
