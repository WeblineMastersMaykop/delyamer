import re
from django import template
from django.template.defaultfilters import stringfilter
from django.http import QueryDict


register = template.Library()

@register.filter
@stringfilter
def only_digits(value):
    if value:
        return re.sub(r'\D', '', value)

register.filter('only_digits', only_digits)


@register.filter
@stringfilter
def split(value):
    return value.split(';')

register.filter('split', split)


@register.filter
@stringfilter
def change_page(value, page):
    get_request = QueryDict(value, mutable=True)
    get_request['page'] = page
    return '?{}'.format(get_request.urlencode())

register.filter('change_page', change_page)


@register.filter
@stringfilter
def change_category(value, category):
    get_request = QueryDict(value, mutable=True)
    get_request['category'] = category
    get_request['page'] = 1
    return '?{}'.format(get_request.urlencode())

register.filter('change_category', change_category)
