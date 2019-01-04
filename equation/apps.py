# Standalone equation block with preview and caption.
# To be used in Wagtail StreamField.
# Adapted from https://github.com/JamesRamm/wagtailmath,
# because that version does not work with Django >- 2.0 and 
# Wagtail 2.3.


from django.apps import AppConfig


class EquationConfig(AppConfig):
    name = 'equation'
