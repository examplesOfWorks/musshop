from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from carts.models import Cart
from orders.models import Order, OrderItem
from .models import DeliveryMethod

from .forms import UserInfoForm, DeliveryForm, PaymentForm

from .phone_utils import format_phone, clean_phone

@login_required
def create_order(request):

    user = request.user
    del_price = DeliveryMethod.objects.filter(name='Доставка').first().price
    delivery_options = DeliveryMethod.objects.all().order_by('id')

    default_delivery = DeliveryMethod.objects.filter(name="Самовывоз", is_active=True).first()
    if default_delivery:
        default_delivery_id = default_delivery.id
    else:
        default_delivery = DeliveryMethod.objects.filter(is_active=True).first()
        default_delivery_id = None

    if request.method == 'POST':
        post_data = request.POST.copy()

        phone = post_data.get('phone_number', '')
        post_data['phone_number'] = clean_phone(phone)

        user_info = UserInfoForm(post_data)
        delivery_info = DeliveryForm(post_data)
        payment_info = PaymentForm(post_data)

        if user_info.is_valid() and delivery_info.is_valid() and payment_info.is_valid():
            try:
                with transaction.atomic():
                    cart_items = Cart.objects.filter(user=user)

                    if not cart_items.exists():
                        raise ValidationError("Корзина пуста.")

                    order = Order.objects.create(
                        user=user,
                        phone_number=user_info.cleaned_data['phone_number'],
                        email=user_info.cleaned_data['email'],
                        delivery_method=delivery_info.cleaned_data['delivery_method'],
                        delivery_address=delivery_info.cleaned_data['delivery_address'],
                        delivery_comment=delivery_info.cleaned_data['delivery_comment'],
                        payment_on_get=payment_info.cleaned_data['payment_on_get'],
                    )

                    for cart_item in cart_items:
                        product = cart_item.product
                        name=cart_item.product.name
                        price=cart_item.product.sell_price()
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(f'Недостаточно товара "{product.name}" в наличии.')
                        
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )

                        product.quantity -= quantity
                        product.save()

                    cart_items.delete()

                    return JsonResponse({'redirect_url': reverse('orders:order_history')})
            except ValidationError as e:
                return JsonResponse({'success': False, 'message': e.message}, status=400)
        
        else:
            errors = {
                'user_errors': user_info.errors,
                'delivery_errors': delivery_info.errors,
                'payment_errors': payment_info.errors,
            }
            return JsonResponse({'success': False, **errors}, status=400)
        
    else:
        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': format_phone(user.phone_number or ''),
        }

        user_info = UserInfoForm(initial=initial)
        delivery_info = DeliveryForm()
        payment_info = PaymentForm()

    context = {
        'title': 'Оформление заказа',
        'body_class': 'checkout_page',
        'delivery_options': delivery_options,
        'del_price': del_price,
        'default_delivery_id': default_delivery_id,
        'user_info': user_info,
        'delivery_info': delivery_info,
        'payment_info': payment_info,
    }
    return render(request, 'orders/create_order.html', context)

def order_history(request):
    page = request.GET.get('page', 1)

    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_timestamp')
    
    paginator = Paginator(orders, 3)
    current_page = paginator.page(int(page))

    context = {
        'title': 'История заказов',
        'body_class': 'shop_page',
        'orders': current_page,
        'all_orders': orders,
    }
    return render(request, 'orders/order_history.html', context)

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    items_sum = sum(order_item.price * order_item.quantity for order_item in order_items)
    context = {
        'title': 'Состав заказа',
        'body_class': 'shop_page',
        'order': order,
        'order_items': order_items,
        'items_sum': items_sum,
    }
    return render(request, 'orders/order_detail.html', context)

def order_delete(request):
    order_id = request.POST.get('order_id')
    order = get_object_or_404(Order, id=order_id, user=request.user, status='processing')
    order.delete()
    return redirect('orders:order_history')