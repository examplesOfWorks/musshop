from django.test import TestCase

from goods.models import Brands, Categories, Subcategories, Types, Products

class CategoriesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Categories.objects.create(
            name="Клавишные инструменты",
            slug="klavishnye-instrumenty"
        )
    
    def test__str__(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_name_max_length(self):
        category = Categories.objects.get(id=self.category.id)
        max_length = category._meta.get_field('name').max_length
        self.assertLessEqual(max_length, 150)

    def test_slug_max_length(self):
        category = Categories.objects.get(id=self.category.id)
        max_length = category._meta.get_field('name').max_length
        self.assertLessEqual(max_length, 200)

    def test_name_unique(self):
        category = Categories.objects.get(id=self.category.id)
        name_unique = category._meta.get_field('name').unique
        self.assertTrue(name_unique)

    def test_slug_unique(self):
        category = Categories.objects.get(id=self.category.id)
        slug_unique = category._meta.get_field('slug').unique
        self.assertTrue(slug_unique)

    def test_slug_blank_and_null(self):
        category = Categories(name='Укулеле и аксессуары')
        category.full_clean()
        category.save()
        self.assertIsNone(category.slug)

    def test_image_blank_and_null(self):
        self.assertIsNone(self.category.image.name)

    def test_ordering(self):
        self.assertEqual(Categories._meta.ordering, ("id",))

class SubcategoriesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Categories.objects.create(
            name="Клавишные инструменты",
            slug="klavishnye-instrumenty"
        )
        cls.subcategory = Subcategories.objects.create(
            name="Цифровые пианино",
            category=cls.category
        )

    def test__str__(self):
        self.assertEqual(str(self.subcategory), "Цифровые пианино")

    def test_verbose_name(self):
        name_field = self.subcategory._meta.get_field('name')
        slug_field = self.subcategory._meta.get_field('slug')
        image_field = self.subcategory._meta.get_field('image')

        self.assertEqual(name_field.verbose_name, "Название")
        self.assertEqual(slug_field.verbose_name, "URL")
        self.assertEqual(image_field.verbose_name, "Изображение")

    def test_max_length(self):
        name_field = self.subcategory._meta.get_field('name')
        slug_field = self.subcategory._meta.get_field('slug')

        self.assertEqual(name_field.max_length, 255)
        self.assertEqual(slug_field.max_length, 255)

    def test_blank_and_null(self):
        self.assertIsNone(self.subcategory.slug)
        self.assertIsNone(self.subcategory.image.name)

    def test_ordering(self):
        self.assertEqual(Subcategories._meta.ordering, ("id",))

    def test_category_field_meta(self):
        field = self.subcategory._meta.get_field('category')
        self.assertEqual(field.verbose_name, "Категория")
        self.assertEqual(field.related_model, Categories)

    def test_foreign_key_relationship(self):
        self.assertEqual(self.subcategory.category.name, "Клавишные инструменты")
        self.assertIsInstance(self.subcategory.category, Categories)
        self.category.delete()
        subcategories = Subcategories.objects.all()
        self.assertEqual(subcategories.count(), 0)
    
class BrandsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.brand = Brands.objects.create(
            name="Yamaha",
        )

    def test__str__(self):
        self.assertEqual(str(self.brand), "Yamaha")

    def test_verbose_name(self):
        name_field = self.brand._meta.get_field('name')
        slug_field = self.brand._meta.get_field('slug')
        image_field = self.brand._meta.get_field('image')

        self.assertEqual(name_field.verbose_name, "Название")
        self.assertEqual(slug_field.verbose_name, "URL")
        self.assertEqual(image_field.verbose_name, "Изображение")

    def test_max_length(self):
        name_field = self.brand._meta.get_field('name')
        slug_field = self.brand._meta.get_field('slug')

        self.assertEqual(name_field.max_length, 150)
        self.assertEqual(slug_field.max_length, 200)

    def test_blank_and_null(self):
        self.assertIsNone(self.brand.slug)
        self.assertIsNone(self.brand.image.name)

    def test_ordering(self):
        self.assertEqual(Brands._meta.ordering, ("id",))

    def test_unique(self):
        name_unique = self.brand._meta.get_field('name').unique
        slug_unique = self.brand._meta.get_field('slug').unique
        self.assertTrue(name_unique)
        self.assertTrue(slug_unique)

class TypesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Categories.objects.create(
            name="Клавишные инструменты",
        )
        cls.subcategory = Subcategories.objects.create(
            name="Цифровые пианино",
            category=cls.category
        )
        cls.type = Types.objects.create(
            name='Бюджетные цифровые пианино',
            subcategory=cls.subcategory
        )
    def test__str__(self):
        self.assertEqual(str(self.type), "Бюджетные цифровые пианино")

    def test_verbose_name(self):
        name_field = self.type._meta.get_field('name')
        slug_field = self.type._meta.get_field('slug')
        subcategory_field = self.type._meta.get_field('subcategory')

        self.assertEqual(name_field.verbose_name, "Название")
        self.assertEqual(slug_field.verbose_name, "URL")
        self.assertEqual(subcategory_field.verbose_name, "Подкатегория")

    def test_max_length(self):
        name_field = self.type._meta.get_field('name')
        slug_field = self.type._meta.get_field('slug')

        self.assertEqual(name_field.max_length, 150)
        self.assertEqual(slug_field.max_length, 200)

    def test_blank_and_null(self):
        self.assertIsNone(self.type.slug)

    def test_ordering(self):
        self.assertEqual(Types._meta.ordering, ("id",))

    def test_subcategory_field_meta(self):
        field = self.type._meta.get_field('subcategory')
        self.assertEqual(field.related_model, Subcategories)

    def test_foreign_key_relationship(self):
        self.assertEqual(self.type.subcategory.name, "Цифровые пианино")
        self.assertIsInstance(self.type.subcategory, Subcategories)
        self.subcategory.delete()
        types = Types.objects.all()
        self.assertEqual(types.count(), 0)

class ProductsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Categories.objects.create(
            name="Клавишные инструменты",
        )
        cls.subcategory = Subcategories.objects.create(
            name="Цифровые пианино",
            category=cls.category
        )
        cls.type = Types.objects.create(
            name='Бюджетные цифровые пианино',
            subcategory=cls.subcategory
        )
        cls.brand = Brands.objects.create(
            name="Yamaha",
        )
        cls.product1 = Products.objects.create(
            name='Товар 1',
            article='111111',
            price=100,
            discount=10,
            quantity=5,
            brand=cls.brand,
            subcategory=cls.subcategory,
            type=cls.type,
        )
        cls.product2 = Products.objects.create(
            name='Товар 2',
            article='222222',
            price=200,
            discount=20,
            quantity=10,
            brand=cls.brand,
            subcategory=cls.subcategory,
        )

    def test__str__(self):
        self.assertEqual(str(self.product1), "Товар 1 Количество - 5")

    def test_verbose_name(self):
        name_field = self.product1._meta.get_field('name')
        article_field = self.product1._meta.get_field('article')
        warranty_field = self.product1._meta.get_field('warranty')
        description_field = self.product1._meta.get_field('description')
        specifications_field = self.product1._meta.get_field('specifications')
        # instructions_field = self.product1._meta.get_field('instructions')
        price_field = self.product1._meta.get_field('price')
        discount_field = self.product1._meta.get_field('discount')
        quantity_field = self.product1._meta.get_field('quantity')
        brand_field = self.product1._meta.get_field('brand')
        subcategory_field = self.product1._meta.get_field('subcategory')
        type_field = self.product1._meta.get_field('type')
        created_timestamp_field = self.product1._meta.get_field('created_timestamp')

        self.assertEqual(name_field.verbose_name, "Название")
        self.assertEqual(article_field.verbose_name, "Артикул")
        self.assertEqual(warranty_field.verbose_name, "Гарантия")
        self.assertEqual(description_field.verbose_name, "Описание")
        self.assertEqual(specifications_field.verbose_name, "Характеристики")
        # self.assertEqual(instructions_field.verbose_name, "Инструкции")
        self.assertEqual(price_field.verbose_name, "Цена")
        self.assertEqual(discount_field.verbose_name, "Скидка в %")
        self.assertEqual(quantity_field.verbose_name, "Количество")
        self.assertEqual(brand_field.verbose_name, "Бренд")
        self.assertEqual(subcategory_field.verbose_name, "Подкатегория")
        self.assertEqual(type_field.verbose_name, "Тип")
        self.assertEqual(created_timestamp_field.verbose_name, "Дата добавления")

    def test_max_length(self):
        name_field = self.product1._meta.get_field('name')
        article_field = self.product1._meta.get_field('article')
        warranty_field = self.product1._meta.get_field('warranty')

        self.assertEqual(name_field.max_length, 150)
        self.assertEqual(article_field.max_length, 150)
        self.assertEqual(warranty_field.max_length, 150)

    def test_blank_and_null(self):
        self.assertIsNone(self.product2.warranty)
        self.assertIsNone(self.product2.specifications)
        # self.assertIsNone(self.product2.instructions.name)
        self.assertIsNone(self.product2.type)

    def test_ordering(self):
        self.assertEqual(Products._meta.ordering, ("id",))

    def test_subcategory_field_meta(self):
        brand_field = self.product1._meta.get_field('brand')
        type_field = self.product1._meta.get_field('type')
        subcategory_field = self.product1._meta.get_field('subcategory')
        self.assertEqual(brand_field.related_model, Brands)
        self.assertEqual(subcategory_field.related_model, Subcategories)
        self.assertEqual(type_field.related_model, Types)

    def test_foreign_key_relationship(self):
        self.assertEqual(self.product1.brand.name, "Yamaha")
        self.assertIsInstance(self.product1.brand, Brands)
        self.assertEqual(self.product1.subcategory.name, "Цифровые пианино")
        self.assertIsInstance(self.product1.subcategory, Subcategories)
        self.assertEqual(self.product1.type.name, "Бюджетные цифровые пианино")
        self.assertIsInstance(self.product1.type, Types)

    def test_delete_brand(self):
        self.brand.delete()
        products = Products.objects.all()
        self.assertEqual(products.count(), 0)

    def test_delete_subcategory(self):
        self.subcategory.delete()
        products = Products.objects.all()
        self.assertEqual(products.count(), 0)

    def test_delete_type(self):
        type_id = self.type.id
        self.type.delete()
        products = Products.objects.filter(type_id=type_id)
        self.assertEqual(products.count(), 0)

    def test_sell_price_with_discount(self):
        self.assertEqual(self.product1.sell_price(), 90.00)

    def test_sell_price_without_discount(self):
        self.product1.discount = 0
        self.assertEqual(self.product1.sell_price(), 100.00)