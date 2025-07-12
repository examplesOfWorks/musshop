from django.core.validators import RegexValidator

from django.db import models

from goods.models import Products
from users.models import User


class OrderitemQueryset(models.QuerySet):
   
    def total_price(self):
        return sum(cart.products_price() for cart in self)
   
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class DeliveryMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name="Способ доставки")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Стоимость доставки", default=0)
    required_address = models.BooleanField(default=False, verbose_name="Требуется адрес доставки")
    is_active = models.BooleanField(default=True, verbose_name="Доступна ли опция")

    class Meta:
        verbose_name = "Способ доставки"
        verbose_name_plural = "Способы доставки"

    def __str__(self):
        return f"{self.name} ({self.price} ₽)"
    
class Order(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^((\+7|7|8)+([0-9]){10})$")

    class StatusChoices(models.TextChoices):
        PROCESSING = 'processing', 'В обработке'
        CONFIRMED = 'confirmed', 'Принят в работу'
        COMPLETED = 'completed', 'Выполнен'
        CANCELED = 'canceled', 'Отменен'

    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Пользователь", default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа" )
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=12)
    email = models.EmailField(max_length=50, verbose_name="Email")
    delivery_method = models.ForeignKey(to=DeliveryMethod, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Способ доставки")
    delivery_address = models.TextField(null=True, blank=True, verbose_name="Адрес доставки")
    delivery_comment = models.TextField(null=True, blank=True, verbose_name="Комментарии к доставке")
    payment_on_get = models.BooleanField(default=False, verbose_name="Оплата при получении")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PROCESSING,
        verbose_name="Статус заказа"
    )

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("id",)

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"

    def get_status_display(self):
        return self.StatusChoices(self.status).label

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, verbose_name="Продукт", default=None)
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")


    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"
        ordering = ("id",)

    objects = OrderitemQueryset.as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"