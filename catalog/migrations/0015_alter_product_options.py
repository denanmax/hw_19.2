# Generated by Django 4.2.4 on 2023-08-29 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_alter_product_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',), 'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
