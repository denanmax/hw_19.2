from datetime import datetime


from django.db import models
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

# Create your models here.

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name='категория')
    description = models.TextField(verbose_name='описание', blank=False)

    def __str__(self):
        return f'{self.name}, {self.description}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    preview_image = models.ImageField(upload_to='product_image/', **NULLABLE, verbose_name='изображение продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1,verbose_name='категория')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_change_date = models.DateTimeField(auto_now=True, **NULLABLE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name},{self.category},{self.price}, {self.creation_date}/{self.last_change_date}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.IntegerField(verbose_name='номер версии')
    version_name = models.CharField(max_length=50, verbose_name='название версии')
    is_current = models.BooleanField(default=True, verbose_name='признак текущей версии', unique=True)

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'



class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    phone = models.IntegerField(unique=True, null=False, blank=False)
    message = models.TextField(verbose_name='message')

    def __str__(self):
        return self.name

def toggle_activity(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    if product_item.is_active:
        product_item.is_active = False
    else:
        product_item.is_active = True

    product_item.save()

    return redirect(reverse('home'))