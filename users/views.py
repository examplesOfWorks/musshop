from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.template.loader import render_to_string
from django.contrib.auth.views import LogoutView

from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from carts.models import Cart
from goods.models import Products
from users.models import Wishlist

from users.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm

from users.utils import get_wishlist_count, get_user_wishlist

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('user:profile')
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)

            if session_key:
                new_carts = Cart.objects.filter(session_key=session_key)
                old_carts = Cart.objects.filter(user=user)
                
                for cart in new_carts:
                    existing_cart = old_carts.filter(product=cart.product).first()

                    if existing_cart:
                        existing_cart.quantity += cart.quantity
                        existing_cart.save()
                        cart.delete()
                    else:
                        cart.user = user
                        cart.session_key = None
                        cart.save()

            messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")
            return HttpResponseRedirect(self.get_success_url())
        
    def form_invalid(self, form):
        messages.error(self.request, "Пользователь не найден")
        return super().form_invalid(form)
    
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')

    @transaction.atomic
    def form_valid(self, form):
        session_key=self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)
        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user, session_key=None)
            
        messages.success(self.request, f"{user.username}, Вы успешно зарегистрировались и вошли в аккаунт")
        return HttpResponseRedirect(self.success_url)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            messages.success(self.request, f"{self.request.user.username}, Вы успешно обновили профиль")
            return JsonResponse({'success': True})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль пользователя'
        context['body_class'] = 'shop_page'
        return context

class UsersCartView(LoginRequiredMixin, TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        context['show_btn'] = True
        return context

class WishlistAddView(View):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            product_id = request.POST.get("product_id")
            product = Products.objects.get(id=product_id)
            in_wishlist = request.POST.get("in_wishlist").lower() == "true"
            if not in_wishlist:
                Wishlist.objects.create(user=user, product=product)
                response_data = {
                    'success': True,
                    'message_ajax': "Товар добавлен в избранное",
                    'wishlist_count': get_wishlist_count(request)
                }
            else:
                Wishlist.objects.filter(user=user, product=product).delete()
                wishlist_products = get_user_wishlist(request)
                wishlist_items_html = render_to_string(
                "users/includes/wishlist_items.html", {"wishlist_products": wishlist_products}, request=request)

                response_data = {
                    'success': True,
                    'message_ajax': "Товар удален из избранного",
                    'wishlist_count': get_wishlist_count(request),
                    'wishlist_items_html': wishlist_items_html
                }
        else:
            response_data = {
                'success': False,
                'message_ajax': "Пожалуйста, авторизируйтесь"
            }
        return JsonResponse(response_data)

class WishlistView(LoginRequiredMixin, ListView):
    template_name = 'users/wishlist.html'
    context_object_name = 'wishlist_products'
    paginate_by = 3

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).order_by('-created_timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Избранное'
        return context

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        username = request.user.username 
        messages.success(request, f"{username}, Вы вышли из аккаунта")
        return super().dispatch(request, *args, **kwargs)