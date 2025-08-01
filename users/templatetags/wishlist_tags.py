from django import template

from users.utils import get_wishlist_count

register = template.Library()

@register.simple_tag()
def user_wishlist(request):
    return get_wishlist_count(request)