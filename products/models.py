from django.db import models
import mptt
from uuid import uuid1
from mptt.models import MPTTModel, TreeForeignKey
from colorfield.fields import ColorField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from core.models import SEO, Position



class Category(MPTTModel, SEO, Position):
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, related_name='children',
                            verbose_name='Родительская категория', blank=True, null=True)
    name = models.CharField('Название', max_length=100)
    code_1c = models.CharField('Код 1с', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('position',)

    def __str__(self):
        return self.name

mptt.register(Category,)


class Color(models.Model):
    code_1c = models.CharField('Код 1с', max_length=20, unique=True, null=True, blank=True)
    name = models.CharField('Название', max_length=100)
    color = ColorField('Цвет', null=True, blank=True)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name


class Size(models.Model):
    # code_1c = models.CharField('Код 1с', max_length=20, unique=True)
    name = models.CharField('Название', max_length=10)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.name


class Cup(models.Model):
    name = models.CharField('Название', max_length=10)

    class Meta:
        verbose_name = 'Размер чашки'
        verbose_name_plural = 'Размеры чашки'

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField('Характеристика', max_length=250)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return self.name


class Product(SEO):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', verbose_name='Категория', null=True, blank=True)
    code_1c = models.CharField('Код 1с', max_length=100, unique=True)
    name = models.CharField('Название', max_length=250)
    vendor_code = models.CharField('Артикул', max_length=20, null=True, blank=True)
    pushup = models.BooleanField('Пуш-ап', default=True)
    price = models.PositiveIntegerField('Цена', default=0)
    desc = models.TextField('Описание', null=True, blank=True)
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


class ProductProperty(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='properties', verbose_name='Товар')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='properties', verbose_name='Характеристика')
    value = models.CharField('Значение', max_length=250)

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товара'
        unique_together = ('product', 'property')

    def __str__(self):
        return '{0} -- {1}'.format(self.product.name, self.property.name)


class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers', verbose_name='Товар')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='offers', verbose_name='Цвет')
    cup = models.ForeignKey(Cup, on_delete=models.CASCADE, related_name='offers', verbose_name='Чашка')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='offers', verbose_name='Размер')
    stock = models.PositiveIntegerField('На складе', default=0)
    sale = models.PositiveIntegerField('Скидка', default=0)
    is_active = models.BooleanField('Показывать на сайте', default=True)
    created = models.DateField('Дата создания', auto_now_add=True)
    updated = models.DateField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Вариант товара'
        verbose_name_plural = 'Варианты товара'
        unique_together = ('product', 'color', 'size', 'cup')

    def __str__(self):
        return '{} -- {} -- {} -- {}'.format(self.product.name, self.color.name, self.size.name, self.cup.name)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='images', verbose_name='Цвет')

    def get_picture_url(self, filename):
        ext = filename.split('.')[-1]
        filename = '{0}.{1}'.format(uuid1(), ext)
        return 'images/products/{0}/{1}'.format(self.product.slug, filename)

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')

    image_big = ImageSpecField(source='image',
                                 processors=[ResizeToFill(696, 870)],
                                 format='JPEG',
                                 options={'quality': 90})

    image_medium = ImageSpecField(source='image',
                                 processors=[ResizeToFill(260, 391)],
                                 format='JPEG',
                                 options={'quality': 90})

    image_small = ImageSpecField(source='image',
                                 processors=[ResizeToFill(648, 110)],
                                 format='JPEG',
                                 options={'quality': 90})

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        unique_together = ('color', 'product')

    def __str__(self):
        return '{0} -- {1}'.format(self.product.name, self.id)


@receiver(pre_delete, sender=ProductImage)
def product_image_delete(sender, instance, **kwargs):
    instance.image.delete(False)
