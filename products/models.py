from django.db import models
import mptt
from mptt.models import MPTTModel, TreeForeignKey
from colorfield.fields import ColorField
from core.models import SEO, Position
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from uuid import uuid1


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


class Property(models.Model):
    # TODO Остановился тут
    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return self.name


class Product(SEO):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField('Название', max_length=250)
    vendor_code = models.CharField('Артикул', max_length=20)
    price = models.PositiveIntegerField('Цена')
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


class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers', verbose_name='Товар')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='offers', verbose_name='Цвет', null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, related_name='offers', verbose_name='Размер', null=True, blank=True)
    stock = models.PositiveIntegerField('На складе', default=0)
    sale = models.PositiveIntegerField('Скидка', default=0)
    is_active = models.BooleanField('Показывать на сайте', default=True)
    created = models.DateField('Дата создания', auto_now_add=True)
    updated = models.DateField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Вариант товара'
        verbose_name_plural = 'Варианты товара'

    def __str__(self):
        return '{0} -- {1} -- {2}'.format(self.product.name, self.color.name, self.size.name)


class OfferImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='images', verbose_name='Вариант товара')

    def get_picture_url(self, filename):
        ext = filename.split('.')[-1]
        filename = '{0}.{1}'.format(uuid1(), ext)
        return 'images/products/{0}/{1}'.format(self.offer.product.slug, filename)

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

    def __str__(self):
        return '{0} -- {1}'.format(self.offer.product.name, self.id)
