from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def get_icon_class(lang):
    icon_class = "devicons devicons-"
    if lang == 'javascript':
        return icon_class + 'nodejs_small'
    if lang in ['c', 'cpp', 'typescript']:
        return "fas fa-code"
    else:
        return icon_class + lang
