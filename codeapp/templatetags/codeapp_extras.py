from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def get_icon_class(lang):
    icon_class = "devicons devicons-"
    if lang == 'javascript' or lang == 'typescript':
        return icon_class + 'nodejs_small'
    if lang == 'c' or lang == 'cpp':
        return "fas fa-code"
    else:
        return icon_class + lang
