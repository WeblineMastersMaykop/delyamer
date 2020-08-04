from django.db import models
import mptt
from mptt.models import MPTTModel, TreeForeignKey
from colorfield.fields import ColorField
from core.models import SEO, Position


class Category(MPTTModel, SEO, Position):
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, related_name='children',
                            verbose_name='Родительская категория', blank=True, null=True)
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('position',)

    def __str__(self):
        return self.name

mptt.register(Category,)


class Color(models.Model):
    name = models.CharField('Название', max_length=100)
    color = ColorField('Цвет')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField('Название', max_length=10)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.name


class Product(SEO):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField('Название', max_length=250)
    price = models.PositiveIntegerField('Цена')
    sale = models.PositiveIntegerField('Скидка', default=0)
    is_active = models.BooleanField('Показывать на сайте', default=True)
    is_new = models.BooleanField('NEW', default=True)
    is_bs = models.BooleanField('ХИТ', default=True)
    created = models.DateField('Дата создания', auto_now_add=True)
    updated = models.DateField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
