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