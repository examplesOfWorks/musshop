from django.test import TestCase
from django.urls import reverse

from goods.models import Brands, Categories, Products, Subcategories, Types
from users.models import User, Wishlist

class CatalogViewTest(TestCase):
    def setUp(self):
        self.brand1 = Brands.objects.create(name='Yamaha', slug='yamaha')
        self.brand2 = Brands.objects.create(name='Casio', slug='casio')

        self.category = Categories.objects.create(name='Клавишные инструменты', slug='klavishnye-instrumenty')
        self.subcategory = Subcategories.objects.create(name='Цифровые пианино', slug='sintezatory', category=self.category)
            
        self.type = Types.objects.create(name='Бюджетные цифровые пианино', slug='bjudzhetnye-tsifrovye-pianino', subcategory=self.subcategory)

        self.product1 = Products.objects.create(
            name = 'Товар 1',
            article = '111111',
            price = 100,
            discount = 10,
            quantity = 5,
            brand = self.brand1,
            subcategory = self.subcategory,
            type = self.type,
        )
            
        self.product2 = Products.objects.create(
            name = 'Товар 2',
            article = '222222',
            price = 200,
            discount = 0,
            quantity = 10,
            brand = self.brand2,
            subcategory = self.subcategory,
            type = self.type,
        )

        self.url = reverse('goods:search', kwargs={'subcategory_slug': self.subcategory.slug})
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_catalog_renders_correctly(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/catalog.html')
        self.assertEqual(response.context['title'], 'Каталог')
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product2, response.context['products'])

    def test_catalog_filters_by_discount(self):
        response = self.client.get(self.url, {'discount': 'true'})
        products = list(response.context['products'])
        self.assertIn(self.product1, products)
        self.assertNotIn(self.product2, products)

    def test_catalog_filters_by_brand(self):
        response = self.client.get(self.url, {'brand': self.brand1.slug})
        products = list(response.context['products'])
        self.assertIn(self.product1, products)
        self.assertNotIn(self.product2, products)

    def test_catalog_sorts_by_price_asc(self):
        response = self.client.get(self.url, {'order_by': 'price'})
        products = list(response.context['products'])
        self.assertEqual(products[0], self.product1)
        self.assertEqual(products[1], self.product2)

    def test_catalog_sorts_by_price_desc(self):
        response = self.client.get(self.url, {'order_by': '-price'})
        products = list(response.context['products'])
        self.assertEqual(products[0], self.product2)
        self.assertEqual(products[1], self.product1)

    def test_in_wishlist_for_user(self):
        self.client.login(username=self.user.username, password='password123')
        Wishlist.objects.create(user=self.user, product=self.product1)
        response = self.client.get(self.url)
        wishlist_ids = response.context['wishlist_product_ids']
        self.assertIn(self.product1.id, wishlist_ids)
        self.assertNotIn(self.product2.id, wishlist_ids)

    def test_pagination(self):
        for i in range(15):
            Products.objects.create(
                name = f'Tовар {i}',
                article = f'111111{i}',
                price = 100,
                discount = 10,
                quantity = 5,
                brand = self.brand1,
                subcategory = self.subcategory,
                type = self.type,
            )
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['products']), 12)


class ProductViewTest(TestCase):
    def setUp(self):
        self.brand = Brands.objects.create(name='Yamaha', slug='yamaha')

        self.category = Categories.objects.create(name='Клавишные инструменты', slug='klavishnye-instrumenty')
        self.subcategory = Subcategories.objects.create(name='Цифровые пианино', slug='sintezatory', category=self.category)
            
        self.type = Types.objects.create(name='Бюджетные цифровые пианино', slug='bjudzhetnye-tsifrovye-pianino', subcategory=self.subcategory)

        self.product1 = Products.objects.create(
            name = 'Товар 1',
            article = '111111',
            price = 100,
            discount = 10,
            quantity = 5,
            brand = self.brand,
            subcategory = self.subcategory,
            type = self.type,
        )
            
        self.product2 = Products.objects.create(
            name = 'Товар 2',
            article = '222222',
            price = 200,
            discount = 20,
            quantity = 10,
            brand = self.brand,
            subcategory = self.subcategory,
            type = self.type,
        )

        self.url = reverse('goods:product', kwargs={'product_article': self.product1.article})
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_get_right_product_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/product.html')
        self.assertEqual(response.context['product'].name, 'Товар 1')
        self.assertNotEqual(response.context['product'].name, 'Товар 2')

    def test_product_in_wishlist_for_guest(self):
        response = self.client.get(self.url)
        self.assertFalse(response.context['in_wishlist'])

    def test_product_in_wishlist_for_user_without_product_in_wishlist(self):
        self.client.login(username=self.user.username, password='password123')
        response = self.client.get(self.url)
        self.assertFalse(response.context['in_wishlist'])

    def test_product_in_wishlist_for_user_with_product_in_wishlist(self):
        self.client.login(username='testuser', password='password123')
        Wishlist.objects.create(user=self.user, product=self.product1)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'goods/product.html')
        self.assertTrue(response.context['in_wishlist'])

class TypeFilterViewTest(TestCase):
    def setUp(self):
        self.brand = Brands.objects.create(name='Yamaha', slug='yamaha')

        self.category = Categories.objects.create(name='Клавишные инструменты', slug='klavishnye-instrumenty')
        self.subcategory = Subcategories.objects.create(name='Цифровые пианино', slug='sintezatory', category=self.category)
        
        self.type1 = Types.objects.create(name='Бюджетные цифровые пианино', slug='bjudzhetnye-tsifrovye-pianino', subcategory=self.subcategory)
        self.type2 = Types.objects.create(name='Компактные цифровые пианино', slug='kompaktnye-tsifrovye-pianino', subcategory=self.subcategory)
        self.type3 = Types.objects.create(name='Профессиональные цифровые пианино', slug='professional-nye-tsifrovye-pianino', subcategory=self.subcategory)

        self.product1 = Products.objects.create(
            name = 'Товар 1',
            article = '111111',
            price = 100,
            discount = 10,
            quantity = 5,
            brand = self.brand,
            subcategory = self.subcategory,
            type = self.type1,
            )
        
        self.product2 = Products.objects.create(
            name = 'Товар 2',
            article = '222222',
            price = 200,
            discount = 20,
            quantity = 10,
            brand = self.brand,
            subcategory = self.subcategory,
            type = self.type1,
            )
        
        self.product3 = Products.objects.create(
            name = 'Товар 3',
            article = '333333',
            price = 300,
            discount = 30,
            quantity = 15,
            brand = self.brand,
            subcategory = self.subcategory,
            type = self.type2,
            )
        
        self.url = reverse('goods:filter_products_by_type')

    def test_filter_product_by_type(self):
        response = self.client.get(self.url, {'type_id': self.type1.id})
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn("Товар 1", data["catalog_html"])
        self.assertIn("Товар 2", data["catalog_html"])
        self.assertNotIn("Товар 3", data["catalog_html"])

    def test_filter_with_invalid_type_id(self):
        response = self.client.get(self.url, {'type_id': 999})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertNotIn("Товар 1", data["catalog_html"])
        self.assertNotIn("Товар 2", data["catalog_html"])
        self.assertNotIn("Товар 3", data["catalog_html"])

    def test_filter_with_type_without_products(self):
        response = self.client.get(self.url, {'type_id': self.type3.id})
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertNotIn("Товар 1", data["catalog_html"])
        self.assertNotIn("Товар 2", data["catalog_html"])
        self.assertNotIn("Товар 3", data["catalog_html"])


class CategoriesViewTest(TestCase):
    def setUp(self):
        Categories.objects.create(name='Укулеле и аксессуары', slug='ukulele-i-aksessuary')
        self.category2 = Categories.objects.create(name='Клавишные инструменты', slug='klavishnye-instrumenty')
    
    def test_get(self):
        response = self.client.get(reverse('goods:categories'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/category.html')
        self.assertContains(response, 'Категории')
        self.assertContains(response, 'Укулеле и аксессуары')
        self.assertContains(response, 'Клавишные инструменты')


class SubcategoriesViewTest(TestCase):
    def setUp(self):
        self.category1 = Categories.objects.create(name='Укулеле и аксессуары', slug='ukulele-i-aksessuary')
        self.category2 = Categories.objects.create(name='Клавишные инструменты', slug='klavishnye-instrumenty')
       
        self.subcategory1 = Subcategories.objects.create(name='Укулеле', slug='ukulele', category=self.category1)
        self.subcategory2 = Subcategories.objects.create(name='Струны', slug='struny', category=self.category1)
        self.subcategory3 = Subcategories.objects.create(name='Синтезаторы', slug='sintezatory', category=self.category2)

    def test_get(self):
        response = self.client.get(reverse('goods:subcategories', kwargs={'category_slug': self.category1.slug}))
        
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'goods/subcategory.html')
        self.assertEqual(response.context['title'], 'Укулеле и аксессуары')

        self.assertIn('subcategories', response.context)
        cat1_subcategories = response.context['subcategories']
        self.assertEqual(list(cat1_subcategories), [self.subcategory1, self.subcategory2])
        self.assertNotIn(self.subcategory3, cat1_subcategories)
