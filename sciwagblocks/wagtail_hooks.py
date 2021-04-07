from django.templatetags.static import static
from django.shortcuts import render
from django.utils.html import format_html, format_html_join

from wagtail.core import hooks


@hooks.register('insert_editor_css', order=101)
def markdownmath_css():
    # Did not manage to make working simplemde and django-markdownx in StreamField
    # simplemde =  format_html('<link rel="stylesheet" href="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css">')
    css_files = [
        'sciwagblocks/markdownx/css/markdownmath.css',
        'sciwagblocks/markdownx/css/codehilite_default.css'
    ]
    html = format_html_join(
        '\n', '<link rel="stylesheet" href="{}">', 
        ((static(filename),) for filename in css_files)
    )
    return html


@hooks.register('insert_editor_js', order=1001)
def mutation_observer():
    """Mutation Observer object to detect changes in the markdown preview div
    and subsequently run MathJax update when the markdownmath field is added.
    To be loaded after MathJax."""
    observer = """
        <script type="text/javascript">
            var observer_config = { attributes: true, childList: true, subtree: true };
            var observer_callback = function(mutationsList, observer) {
                MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
            };
            var mutation_observer = new MutationObserver(observer_callback);
        </script>
    """
    return observer


@hooks.register('insert_editor_js', order=102)
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