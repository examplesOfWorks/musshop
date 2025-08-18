from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField

class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    image = models.ImageField(upload_to='categories_images', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ("id",)

    def __str__(self):
        return self.name
    
class Subcategories(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, blank=True, null=True, verbose_name='URL')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(max_length=255, upload_to='subcategories_images', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        db_table = 'subcategory'
        verbose_name = 'Подкатегорию'
        verbose_name_plural = 'Подкатегории'
        ordering = ("id",)

    def __str__(self):
        return self.name

class Brands(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    image = models.ImageField(upload_to='brands_images', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        db_table = 'brand'
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ("id",)

    def __str__(self):
        return self.name

class Types(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    subcategory = models.ForeignKey(to=Subcategories, on_delete=models.CASCADE, verbose_name='Подкатегория')

    class Meta:
        db_table = 'type'
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
        ordering = ("id",)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    article = models.CharField(max_length=150, unique=True, verbose_name='Артикул')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    warranty = models.CharField(max_length=150, blank=True, null=True, verbose_name='Гарантия')
    description = ArrayField(models.TextField(), blank=True, null=True, default=list, verbose_name='Описание')
    specifications = models.JSONField(blank=True, null=True, verbose_name="Характеристики")
    instructions = models.FileField(upload_to='goods_instructions', blank=True, null=True, verbose_name='Инструкции')
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Цена')
    discount =  models.DecimalField(default=0.00, max_digits=4, decimal_places=0, verbose_name='Скидка в %')
    quantity = models.PositiveBigIntegerField(default=0.00, verbose_name='Количество')
    brand = models.ForeignKey(to=Brands, on_delete=models.CASCADE, verbose_name='Бренд')
    subcategory = models.ForeignKey(to=Subcategories, on_delete=models.CASCADE, verbose_name='Подкатегория')
    type = models.ForeignKey(to=Types, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Тип')

    class Meta:
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ("id",)

    def __str__(self):
        return f'{self.name} Количество - {self.quantity}'
    
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    
    def display_id(self):
        return f"{self.id:05}"
    
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100, 2)
        return self.price
    
class Gallery(models.Model):
    image = models.ImageField(upload_to='goods_images', verbose_name='Изображение')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')

