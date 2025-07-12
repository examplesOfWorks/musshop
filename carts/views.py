from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string

from goods.models import Products
from carts.models import Cart
from carts.utils import get_user_carts

@csrf_protect
def cart_add(request):
    
    product_id = request.POST.get("product_id")
    product = Products.objects.get(id=product_id)

    product_qty = request.POST.get("product_qty")

    if product_qty:
        qty = int(product_qty)
    else:
        qty = 1

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += qty
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=qty)
    else:
        carts = Cart.objects.filter(
            session_key=request.session.session_key, product=product)
        
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += qty
                cart.save()
        else:
            Cart.objects.create(
                 session_key=request.session.session_key, product=product, quantity=qty)

    user_cart = get_user_carts(request)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)
    
    modal_cart_items_html = render_to_string(
        "carts/includes/modal_cart.html", {"carts": user_cart}, request=request)

    response_data = {
        "cart_items_html": cart_items_html,
        "modal_cart_items_html": modal_cart_items_html,
        "qty": qty,
    }

    return JsonResponse(response_data)

@csrf_protect
def cart_change(request):
    quantity = request.POST.get("quantity")

    user_cart = get_user_carts(request)

    try:
        cart_id = request.POST.get("cart_id")

        cart = Cart.objects.get(id=cart_id)

        cart.quantity = quantity
        cart.save()
        updated_quantity = cart.quantity

        message = ""
        qty = 0

    except Cart.DoesNotExist:
        updated_quantity = 0
        qty = user_cart.total_quantity()
        message = "Позиция ранее уже была удалена"

    finally:

        context = {"carts": user_cart, 'show_btn': True, 'title': 'Корзина'}

        cart_items_html = render_to_string(
            "carts/includes/included_cart.html", context, request=request)
        
        modal_cart_items_html = render_to_string(
            "carts/includes/modal_cart.html", context, request=request)
        
        total = render_to_string(
            "carts/includes/total.html", context, request=request)

        response_data = {
            "cart_items_html": cart_items_html,
            "modal_cart_items_html": modal_cart_items_html,
            "total": total,
            "quantity": updated_quantity,
            "message": message,
            "qty": qty,
        }

    return JsonResponse(response_data)

@csrf_protect
def cart_remove(request):
    user_cart = get_user_carts(request)

    try:
        cart_id = request.POST.get("cart_id")
        cart = Cart.objects.get(id=cart_id)

        quantity = cart.quantity
        cart.delete()

        message = ""
        qty = 0

    except Cart.DoesNotExist:
        qty = user_cart.total_quantity()
        quantity = 0
        message = "Позиция ранее уже была удалена"

    finally:
        context = {"carts": user_cart, 'show_btn': True, 'title': 'Корзина'}

        cart_items_html = render_to_string(
            "carts/includes/included_cart.html", context, request=request)
        
        modal_cart_items_html = render_to_string(
            "carts/includes/modal_cart.html", context, request=request)
            
        total = render_to_string(
            "carts/includes/total.html", context, request=request)


        response_data = {
            "cart_items_html": cart_items_html,
            "modal_cart_items_html": modal_cart_items_html,
            "total": total,
            "quantity_deleted": quantity,
            "message": message,
            "qty": qty,
            "show_btn": True,
        }

    return JsonResponse(response_data)