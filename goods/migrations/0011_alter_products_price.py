# Generated by Django 4.2.7 on 2025-04-26 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0010_alter_subcategories_image_alter_subcategories_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Цена'),
        ),
    ]
