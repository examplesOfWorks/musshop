from django import template
from django.utils.http import urlencode

from orders.models import OrderItem

register = template.Library()


@register.filter
def item_total(price, quantity):
    try:
        return float(price) * int(quantity)
    except (ValueError, TypeError):
        return 'Не удалось подсчитать'

@register.filter
def order_total(items_sum, delevery_price):
    try:
        return float(items_sum) + float(delevery_price)
    except (ValueError, TypeError):
        return 'Не удалось подсчитать'
 
@register.filter
def items_sum(order):
    try:
        order_items = OrderItem.objects.filter(order=order)
        return sum(order_item.price * order_item.quantity for order_item in order_items)
    except (ValueError, TypeError):
        return 'Не удалось подсчитать'
    
@register.filter
def add_delivery(total_items_sum, delevery_price):
    try:
        return float(total_items_sum) + float(delevery_price)
    except (ValueError, TypeError):
        return 'Не удалось подсчитать'
    
@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
