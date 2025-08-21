from django import template
from django.utils.http import urlencode
from users.utils import get_wishlist_count

register = template.Library()

@register.simple_tag()
def user_wishlist(request):
    return get_wishlist_count(request)

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)