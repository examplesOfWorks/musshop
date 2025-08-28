from django import template

from common.filters import format_phone

register = template.Library()

@register.filter()
def format_phone_tag(value):
    return format_phone(value)