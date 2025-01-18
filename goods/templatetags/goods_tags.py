from django import template
from django.utils.http import urlencode

from goods.models import Categories, Subcategories
from goods.views import subcategories

register = template.Library()


@register.simple_tag()
def tag_all_categories():
    categories = Categories.objects.all()
    all_categories = []
    for category in categories:
        subcategory = Subcategories.objects.filter(category_id=category.id)
        all_categories.append({'category': category, 'subcategory': subcategory})
    return all_categories