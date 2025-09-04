from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from carts.models import Cart
from goods.models import Products, Brands, Categories, Subcategories
from users.models import User
from orders.models import DeliveryMethod, Order

from orders.forms import UserInfoForm


class CreateOrderView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
        first_name = 'testname',
        last_name = 'testlastname',
        username = 'testuser',
        phone_number="+79999999999",
        email = 'testemail@example.com',
        password = 'testuserpassword123',
        )

        self.format_phone_number = '+7(999)999-9999'

        self.client.login(username="testuser", password="testuserpassword123")

        self.pickup = DeliveryMethod.objects.create(name="Самовывоз", price=0, is_active=True)
        self.delivery = DeliveryMethod.objects.create(name="Доставка", price=300, is_active=True, required_address=True)

        self.url = reverse("orders:create_order")

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

        self.cart = Cart.objects.create(user=self.user, product=self.product, quantity=1)

    def test_get_create_order_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/create_order.html")
        self.assertIn("delivery_options", response.context)
        self.assertIn("del_price", response.context)
        self.assertIn("default_delivery_id", response.context)
        self.assertIn("user_info", response.context)
        self.assertIn("delivery_info", response.context)
        self.assertIn("payment_info", response.context)
        self.assertIsInstance(response.context["user_info"], UserInfoForm)

    def test_creates_order_with_invalid_data(self):
        response = self.client.post(self.url, {
            "first_name": "",
            "last_name": "",
            "email": "testemail@",
            "phone_number": self.format_phone_number,
            "delivery_method": '',
            "payment_on_get": '0',
        })

        self.assertEqual(response.status_code, 400)

        data = response.json()

        self.assertIn("user_errors", data)
        self.assertIn("first_name", data["user_errors"])
        self.assertEqual(data["user_errors"]["first_name"], ["Обязательное поле."])

        self.assertIn("last_name", data["user_errors"])
        self.assertEqual(data["user_errors"]["last_name"], ["Обязательное поле."])

        self.assertIn("email", data["user_errors"])
        self.assertEqual(data["user_errors"]["email"], ["Введите правильный адрес электронной почты."])

        self.assertIn("delivery_errors", data)
        self.assertIn("delivery_method", data["delivery_errors"])
        self.assertEqual(data["delivery_errors"]["delivery_method"], ["Обязательное поле."])

        self.assertFalse(response.json()["success"])

    def test_creates_order_with_valid_data(self):
        delivery_method = DeliveryMethod.objects.get(name="Самовывоз")

        response = self.client.post(self.url, {
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "phone_number": self.format_phone_number,
            "delivery_method": delivery_method.id,
            "payment_on_get": '0',
        })

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("redirect_url", data)

        self.assertEqual(Order.objects.count(), 1)
        
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Заказ успешно оформлен" in str(m) for m in messages))

    def test_creates_order_with_delivery_and_no_address(self):
        delivery_method = DeliveryMethod.objects.get(name="Доставка")

        response = self.client.post(self.url, {
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "phone_number": self.format_phone_number,
            "delivery_method": delivery_method.id,
            "payment_on_get": '0',
        })

        self.assertEqual(response.status_code, 400)

        data = response.json()

        self.assertIn("delivery_errors", data)
        self.assertIn("delivery_address", data["delivery_errors"])
        self.assertEqual(data["delivery_errors"]["delivery_address"], ["Укажите адрес доставки."])
