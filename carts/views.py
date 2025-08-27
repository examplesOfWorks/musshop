from django.http import JsonResponse
from django.views import View

from carts.models import Cart
from carts.utils import get_user_carts
from carts.mixins import CartMixin

from goods.models import Products


class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        product_qty = request.POST.get("product_qty")
        product = Products.objects.get(id=product_id)

        cart = self.get_cart(request, product=product)

        if product_qty:
            qty = int(product_qty)
        else:
            qty = 1

        if cart:
            cart.quantity += qty
            cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None,
                product=product, quantity=qty)
            
        response_data = {
            "qty": qty,
            "message_ajax": "Товар добавлен в корзину",
            "cart_items_html": self.render_cart(request).get('cart_items_html'),
            "modal_cart_items_html": self.render_cart(request).get('modal_cart_items_html'),
        }
        
        return JsonResponse(response_data)

class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart = self.get_cart(request, cart_id=cart_id)
        message_ajax = ""

        if cart:
            cart.quantity = request.POST.get("quantity")
            cart.save()
            quantity = cart.quantity
        else:
            quantity = 0
            message_ajax = "Позиция ранее уже была удалена"

        response_data = {
            "quantity": quantity,
            "qty": get_user_carts(request).total_quantity(),
            "cart_items_html": self.render_cart(request).get('cart_items_html'),
            "modal_cart_items_html": self.render_cart(request).get('modal_cart_items_html'),
            "total": self.render_cart(request).get('total'),
            "message_ajax": message_ajax
        }

        return JsonResponse(response_data)

class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart = self.get_cart(request, cart_id=cart_id)

        if cart:
            cart.quantity = request.POST.get("quantity")
            cart.delete()
            quantity = cart.quantity
            message_ajax = "Товар удален из корзины"
        else:
            quantity = 0
            message_ajax = "Позиция ранее уже была удалена"

        response_data = {
            "quantity": quantity,
            "qty": get_user_carts(request).total_quantity(),
            "cart_items_html": self.render_cart(request).get('cart_items_html'),
            "modal_cart_items_html": self.render_cart(request).get('modal_cart_items_html'),
            "total": self.render_cart(request).get('total'),
            "message_ajax": message_ajax
        }

        return JsonResponse(response_data)