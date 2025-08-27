from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView
from django.contrib import messages

from carts.models import Cart
from orders.models import Order, OrderItem
from .models import DeliveryMethod

from .forms import UserInfoForm, DeliveryForm, PaymentForm

class CreateOrderView(LoginRequiredMixin, View):
    template_name = 'orders/create_order.html'

    # вызов шаблона
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        context['title'] = 'Оформление заказа'
        context['body_class'] = 'checkout_page'

        return render(request, self.template_name, context)
    
    # обработка заказа
    def post(self, request, *args, **kwargs):
        user = request.user
        user_info, delivery_info, payment_info = self.get_forms(request.POST)
    
        if not self.forms_are_valid(user_info, delivery_info, payment_info):
            return JsonResponse({
                'success': False,
                'user_errors': user_info.errors,
                'delivery_errors': delivery_info.errors,
                'payment_errors': payment_info.errors,
            }, status=400)
        
        try:
            self.create_order(user, user_info, delivery_info, payment_info)
            messages.success(self.request, "Заказ успешно оформлен. Спасибо за покупку!")
            return JsonResponse({'redirect_url': reverse('orders:order_history')})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message_ajax': e.message}, status=400)

    # формирование данных для шаблона
    def get_context_data(self, request):
        user = request.user
        delivery_options = DeliveryMethod.objects.all().order_by('id')
        del_price = DeliveryMethod.objects.filter(name='Доставка').first().price

        default_delivery = DeliveryMethod.objects.filter(name="Самовывоз", is_active=True).first()
        default_delivery_id = default_delivery.id if default_delivery else None

        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number
        }

        return {
            'delivery_options': delivery_options,
            'del_price': del_price,
            'default_delivery_id': default_delivery_id,
            'user_info': UserInfoForm(initial=initial),
            'delivery_info': DeliveryForm(),
            'payment_info': PaymentForm(),
        }
    
    # создание форм
    def get_forms(self, data):
        return UserInfoForm(data), DeliveryForm(data), PaymentForm(data)
    
    # проверка валидности всех форм
    def forms_are_valid(self, *forms):
        return all([form.is_valid() for form in forms])
    
    # создание заказа и его элементов
    def create_order(self, user, user_info, delivery_info, payment_info):
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            raise ValidationError("Корзина пуста.")

        with transaction.atomic():
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

                if product.quantity < cart_item.quantity:
                    raise ValidationError(f'Недостаточно товара "{product.name}" в наличии.')
                            
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    name=product.name,
                    price=product.sell_price(),
                    quantity=cart_item.quantity,
                )

                product.quantity -= cart_item.quantity
                product.save()

            cart_items.delete()

        return order

class OrderHistoryView(LoginRequiredMixin, ListView):
    template_name = 'orders/order_history.html'
    context_object_name = 'orders'
    paginate_by = 3

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'История заказов'
        context['body_class'] = 'shop_page'
        return context

class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_object(self, queryset = None):
        order = Order.objects.get(id=self.kwargs.get('order_id'))
        return order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        order_items = OrderItem.objects.filter(order=order)
        items_sum = sum(order_item.price * order_item.quantity for order_item in order_items)
        context['title'] = f'Заказ № {order.id}'
        context['order_items'] = order_items
        context['items_sum'] = items_sum
        return context

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    pk_url_kwarg = 'order_id'
    success_url = reverse_lazy('orders:order_history')

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='processing')
    
    def form_valid(self, form):
        order_id = self.get_object().id
        response = super().form_valid(form)
        messages.success(self.request, f"Заказ №{order_id} успешно удалён.")
        return response