from django.urls import reverse
from django.test import TestCase

from goods.models import Brands, Categories, Subcategories, Products
from carts.models import Cart
from users.models import User

class CartAddViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password123'
        self.phone_number = '+79999999999'
        self.user = User.objects.create_user(username=self.username, password=self.password, phone_number=self.phone_number)

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

        self.url = reverse("cart:cart_add")

    def test_add_to_cart_as_guest_from_catalog_page(self):
        session = self.client.session
        session_key = session.session_key
        product = Products.objects.get(id=self.product.id)

        response = self.client.post(self.url, {'product_id': self.product.id, 'product': product})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["qty"], 1)
        self.assertIn("Товар добавлен в корзину", data["message_ajax"])
        self.assertIn("cart_items_html", data)
        self.assertIn("modal_cart_items_html", data)

        cart_item = Cart.objects.get(product=self.product, session_key=session_key)
        self.assertEqual(cart_item.quantity, 1)


    def test_add_to_cart_as_guest_from_product_page(self):
        session = self.client.session
        session_key = session.session_key
        product = Products.objects.get(id=self.product.id)
        response = self.client.post(self.url, {'product_id': self.product.id, 'product_qty': 2, 'product': product}, follow=True)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["qty"], 2)
        self.assertIn("Товар добавлен в корзину", data["message_ajax"])
        self.assertIn("cart_items_html", data)
        self.assertIn("modal_cart_items_html", data)

        cart_item = Cart.objects.get(product=self.product, session_key=session_key)
        self.assertEqual(cart_item.quantity, 2)

    def test_add_to_cart_as_user_from_catalog_page(self):
        self.client.login(username=self.username, password=self.password)
        product = Products.objects.get(id=self.product.id)

        response = self.client.post(self.url, {'product_id': self.product.id, 'product': product})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["qty"], 1)
        self.assertIn("Товар добавлен в корзину", data["message_ajax"])
        self.assertIn("cart_items_html", data)
        self.assertIn("modal_cart_items_html", data)

        cart_item = Cart.objects.get(product=self.product, user=self.user)
        self.assertEqual(cart_item.quantity, 1)

    def test_add_to_cart_as_user_from_product_page(self):
        self.client.login(username=self.username, password=self.password)
        product = Products.objects.get(id=self.product.id)
        response = self.client.post(self.url, {'product_id': self.product.id, 'product_qty': 2, 'product': product}, follow=True)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["qty"], 2)
        self.assertIn("Товар добавлен в корзину", data["message_ajax"])
        self.assertIn("cart_items_html", data)
        self.assertIn("modal_cart_items_html", data)

        cart_item = Cart.objects.get(product=self.product, user=self.user)
        self.assertEqual(cart_item.quantity, 2)