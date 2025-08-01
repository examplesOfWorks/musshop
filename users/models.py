from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.validators import RegexValidator


class User(AbstractUser):
    phoneNumberRegex = RegexValidator(regex=r"^((\+7|7|8)+([0-9]){10})$")
    phone_number = models.CharField(validators=[phoneNumberRegex], max_length=12, blank=True, null=True)

    class Meta:
        db_table = 'User'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    
class Wishlist(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="wishlist_items", verbose_name='Пользователь')
    product = models.ForeignKey(to='goods.Products', on_delete=models.CASCADE, verbose_name='Товар')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'wishlist'
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        ordering = ("id",)
        
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product')
        ]