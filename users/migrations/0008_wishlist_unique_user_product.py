# Generated by Django 4.2.7 on 2025-07-25 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_wishlist'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='wishlist',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='unique_user_product'),
        ),
    ]
