# Generated by Django 4.2.4 on 2023-08-24 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_rename_is_active_version_is_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='is_current',
            field=models.BooleanField(default=True, unique=True, verbose_name='признак текущей версии'),
        ),
    ]
