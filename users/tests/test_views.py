from django.test import TestCase
from django.urls import reverse

from django.contrib.messages import get_messages

from goods.models import Brands, Categories, Subcategories, Products
from carts.models import Cart
from users.models import User

class LoginViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password123'
        self.phone_number = '+79999999999'
        self.user = User.objects.create_user(username=self.username, password=self.password, phone_number=self.phone_number)

        self.login_url = reverse('user:login')

        self.brand = Brands.objects.create(name='Yamaha', slug='yamaha')
        self.category = Categories.objects.create(name='Клавишные инструменты', slug='klavishnye-instrumenty')
        self.subcategory = Subcategories.objects.create(name='Цифровые пианино', slug='sintezatory', category=self.category)
        self.product = Products.objects.create(
            name = 'Товар 1',
            article = '111111',
            price = 100,
            discount = 10,
            quantity = 5,
            brand = self.brand,
            subcategory = self.subcategory,
        )

    def test_get_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, 'Авторизация')

    def test_successful_login_redirects_to_profile(self):
        response = self.client.post(self.login_url, {
            'username': self.user.username,
            'password': self.password
        })
        self.assertRedirects(response, '/user/profile/')

    def test_next_does_not_redirect_to_logout(self):
        logout_url = reverse('user:logout')
        response = self.client.post(f"{self.login_url}?next={logout_url}", {
            'username': self.user.username,
            'password': self.password
        })
        self.assertRedirects(response, '/user/profile/')

    def test_cart_on_login(self):
        session = self.client.session
        session_key = session.session_key

        Cart.objects.create(session_key=session_key, product=self.product, quantity=2)
        Cart.objects.create(user=self.user, product=self.product, quantity=3)

        response = self.client.post(self.login_url, {
            'username': self.user.username,
            'password': self.password
        })

        cart_item = Cart.objects.get(user=self.user, product=self.product)
        self.assertEqual(cart_item.quantity, 5)

        carts = Cart.objects.filter(user=self.user, product=self.product)
        self.assertEqual(carts.count(), 1)

        self.assertIsNone(cart_item.session_key)
        self.assertEqual(response.status_code, 302)

    def test_message_after_login(self):
        response = self.client.post(self.login_url, {
            'username': self.user.username,
            'password': self.password
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Вы вошли в аккаунт" in str(message) for message in messages))


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.first_name = 'testname'
        self.last_name = 'testlastname'
        self.username = 'testuser'
        self.phone_number = '+7(999)999-9999'
        self.email = 'testemail@example.com'
        self.password = 'testuserpassword123'

        self.registration_url = reverse('users:registration')

        self.brand = Brands.objects.create(name='Yamaha', slug='yamaha')
        self.category = Categories.objects.create(name='Клавишные инструменты', slug='klavishnye-instrumenty')
        self.subcategory = Subcategories.objects.create(name='Цифровые пианино', slug='sintezatory', category=self.category)
        self.product = Products.objects.create(
            name = 'Товар 1',
            article = '111111',
            price = 100,
            discount = 10,
            quantity = 5,
            brand = self.brand,
            subcategory = self.subcategory,
        )

    def _get_form_data(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'phone_number': self.phone_number,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        }

    def test_get_registration_page(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertContains(response, 'Регистрация')

    def test_registration(self):
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.client.post(self.registration_url, self._get_form_data(), follow=True)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_redirects_to_profile(self):
        response = self.client.post(self.registration_url, self._get_form_data(), follow=True)
        self.assertRedirects(response, '/user/profile/')

    def test_registration_with_cart(self):
        session = self.client.session
        session_key = session.session_key

        Cart.objects.create(session_key=session_key, product=self.product, quantity=2)

        self.client.post(self.registration_url, self._get_form_data(), follow=True)
        user = User.objects.get(username=self.username)

        cart_item = Cart.objects.get(user=user, product=self.product)
        self.assertEqual(cart_item.quantity, 2)

        carts = Cart.objects.filter(user=user, product=self.product)
        self.assertEqual(carts.count(), 1)
        self.assertIsNone(cart_item.session_key)

    def test_registration_message(self):
        response = self.client.post(self.registration_url, self._get_form_data(), follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Вы успешно зарегистрировались и вошли в аккаунт" in str(message) for message in messages))