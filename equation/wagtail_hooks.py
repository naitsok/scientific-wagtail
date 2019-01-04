from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render
from django.utils.html import format_html, format_html_join

from wagtail.core import hooks


# @hooks.register('insert_editor_js', order=201)
def mathjax_js():
    # simplemde = format_html('<script src="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.js"></script>')
    mathjax_config = """
        <script type="text/x-mathjax-config">
            MathJax.Hub.Config({
                extensions: ["tex2jax.js"],
                jax: ["input/TeX", "output/HTML-CSS"],
                tex2jax: {
                    inlineMath: [['$','$']],
                    displayMath: [['$$','$$']] ,
                    processEscapes: true
                },
                "HTML-CSS": { 
                    availableFonts: ["TeX"],
                    linebreaks:  { automatic: true }
                }
            });
        </script>
    """
    
    mathjax = '<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js" async></script>'

    return mathjax_config + mathjax # + simplemde


# Ugly solution to prevent placing mathjax twice in admin.
# There is possiblity to put the required script in the widget, but
# no possibility to put MathJax configuration there.
# Is there a better way to not register similar hooks twice?
found = False
editor_js_hooks = hooks.get_hooks('insert_editor_js')
if editor_js_hooks:
    for hook in editor_js_hooks:
        if hook.__name__ == mathjax_js.__name__:
            found=True

if not found:
    hooks.register('insert_editor_js', fn=mathjax_js, order=201)