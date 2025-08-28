from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import DetailView, ListView
from django.db.models import F, ExpressionWrapper, DecimalField

from goods.models import Brands, Categories, Subcategories, Products, Types
from goods.search_utils import q_search

from common.mixins import CacheMixin

class CatalogView(CacheMixin, ListView):
    template_name = 'goods/catalog.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        subcategory_slug = self.kwargs.get('subcategory_slug')
        on_sale = self.request.GET.get('discount')
        order_by = self.request.GET.get('order_by')
        query = self.request.GET.get('q')

        self.filter_brand: list[str] = self.request.GET.getlist('brand')

        if self.request.user.is_authenticated:
            self.wishlist_product_ids = set(
                self.request.user.wishlist_items.values_list("product_id", flat=True)
            )
        else:
            self.wishlist_product_ids = set()

        if query:
            products = q_search(query)
        else:
            products = Products.objects.filter(subcategory__slug=subcategory_slug)

        if on_sale:
            products = products.filter(discount__gt=0)

        if self.filter_brand:
            products = products.filter(brand__slug__in=self.filter_brand)

        products = products.annotate(
        final_price=ExpressionWrapper(
            F('price') - (F('price') * F('discount') / 100),
            output_field=DecimalField(max_digits=9, decimal_places=2)
            )
        )

        if order_by == 'price':
            products = products.order_by('final_price')
        elif order_by == '-price':
            products = products.order_by('-final_price')
        elif order_by and order_by != "default":
            products = products.order_by(order_by)
        
        self.products = products
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        brands = Brands.objects.filter(products__in=self.products).distinct()
        context['brands'] = self.set_get_cache(brands, f'catalog_brands_{self.kwargs.get("subcategory_slug")}', 60 * 2)
        context['subcategory_slug'] = self.kwargs.get('subcategory_slug')
        context['subcategory_types'] = Types.objects.filter(subcategory__slug=self.kwargs.get('subcategory_slug'))
        context['wishlist_product_ids'] = self.wishlist_product_ids
        context['filter_brand'] = self.filter_brand
        return context

class TypeFilterView(View):
    def get(self, request, *args, **kwargs):
        type_id = request.GET.get('type_id')
        products = Products.objects.filter(type=type_id)

        catalog_html = render_to_string('goods/includes/included_catalog.html', {'products': products}, request=request)
        return JsonResponse({'catalog_html': catalog_html})

class ProductView(DetailView):
    template_name = 'goods/product.html'
    slug_url_kwarg = 'product_article'
    context_object_name = 'product'

    def get_object(self, queryset = None):
        product = Products.objects.get(article=self.kwargs.get(self.slug_url_kwarg))
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        user    = self.request.user

        if user.is_authenticated:
            in_wishlist = user.wishlist_items.filter(product_id=product.id).exists()
        else:
            in_wishlist = False

        context['title'] = self.object.name
        context['in_wishlist'] = in_wishlist
        return context

class CategoriesView(ListView):
    model = Categories
    template_name = 'goods/category.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        return context

class SubcategoriesView(ListView):
    model = Subcategories
    template_name = 'goods/subcategory.html'
    context_object_name = 'subcategories'

    def get_queryset(self):
        self.category = Categories.objects.get(slug=self.kwargs.get('category_slug'))
        return Subcategories.objects.filter(category=self.category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.category.name
        return context
