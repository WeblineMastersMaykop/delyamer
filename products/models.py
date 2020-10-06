from django.db import models
from django.urls import reverse
from uuid import uuid1
from colorfield.fields import ColorField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from core.models import SEO, Position
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(SEO, Position):
    name = models.CharField('Название', max_length=100)
    code_1c = models.CharField('Код 1с', max_length=20, unique=True)

    def get_picture_url(self, filename):
        ext = filename.split('.')[-1]
        filename = '{0}.{1}'.format(uuid1(), ext)
        return 'images/categories/{}'.format(filename)

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение', null=True, blank=True)

    image_small = ImageSpecField(source='image',
                                 processors=[ResizeToFill(261, 424)],
                                 format='JPEG',
                                 options={'quality': 90})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('position',)

    def get_absolute_url(self):
        return '{}?category={}'.format(reverse('products'), self.slug)

    def get_products(self):
        return self.products.filter(is_active=True)

    def __str__(self):
        return self.name


class Color(Position):
    code_1c = models.CharField('Код 1с', max_length=20, unique=True, null=True, blank=True)
    name = models.CharField('Название', max_length=100)
    color = ColorField('Цвет', null=True, blank=True)
    is_multi = models.BooleanField('Мультицвет', default=False)

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ('position',)

    def __str__(self):
        return self.name


class Size(Position):
    name = models.CharField('Название', max_length=10)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ('position',)

    def __str__(self):
        return self.name


class Cup(Position):
    name = models.CharField('Название', max_length=10)

    class Meta:
        verbose_name = 'Размер чашки'
        verbose_name_plural = 'Размеры чашки'
        ordering = ('position',)

    def __str__(self):
        return self.name


class Product(SEO):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='Категория')
    code_1c = models.CharField('Код 1с', max_length=100, unique=True)
    name = models.CharField('Название', max_length=250)
    vendor_code = models.CharField('Артикул', max_length=20, null=True, blank=True)
    pushup = models.BooleanField('Пуш-ап', null=True, blank=True)
    price = models.PositiveIntegerField('Цена', default=0)
    desc = models.TextField('Описание', null=True, blank=True)
    is_active = models.BooleanField('Показывать на сайте', default=True)
    is_new = models.BooleanField('NEW', default=False)
    is_bs = models.BooleanField('ХИТ', default=False)
    created = models.DateField('Дата создания', auto_now_add=True)
    updated = models.DateField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse('product', args=[self.slug])

    def get_colors(self, *args, **kwargs):
        size_id = kwargs.get('size_id')
        cup_id = kwargs.get('cup_id')
        offers = self.offers.filter(is_active=True).select_related('color', 'size', 'cup')

        if size_id:
            offers = offers.filter(size__id=size_id)
        if cup_id:
            offers = offers.filter(cup__id=cup_id)

        return sorted(list(set(offer.color for offer in offers if offer.color is not None)), key=lambda color: color.position)

    def get_sizes(self, *args, **kwargs):
        color_id = kwargs.get('color_id')
        cup_id = kwargs.get('cup_id')
        offers = self.offers.filter(is_active=True).select_related('color', 'size', 'cup')

        if cup_id:
            offers = offers.filter(cup__id=cup_id)
        if color_id:
            offers = offers.filter(color__id=color_id)

        return sorted(list(set(offer.size for offer in offers if offer.size is not None)), key=lambda size: size.position)

    def get_cups(self, *args, **kwargs):
        size_id = kwargs.get('size_id')
        color_id = kwargs.get('color_id')
        offers = self.offers.filter(is_active=True).select_related('color', 'size', 'cup')

        if size_id:
            offers = offers.filter(size__id=size_id)
        if color_id:
            offers = offers.filter(color__id=color_id)

        return sorted(list(set(offer.cup for offer in offers if offer.cup is not None)), key=lambda cup: cup.position)

    def main_offer(self):
        main_offer = self.offers.filter(is_active=True).select_related('promotion_sale', 'color', 'size', 'cup').order_by('promotion_sale__sale').last()

        if not main_offer:
            main_offer = self.offers.filter(is_active=True).select_related('color', 'size', 'cup').first()
        return main_offer

    def __str__(self):
        return self.name


class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers', verbose_name='Товар')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='offers', verbose_name='Цвет', null=True, blank=True)
    cup = models.ForeignKey(Cup, on_delete=models.CASCADE, related_name='offers', verbose_name='Чашка', null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='offers', verbose_name='Размер', null=True, blank=True)
    stock = models.PositiveIntegerField('На складе', default=0)
    is_active = models.BooleanField('Показывать на сайте', default=True)
    created = models.DateField('Дата создания', auto_now_add=True)
    updated = models.DateField('Дата изменения', auto_now=True)

    promotion_sum_present = models.ForeignKey('promotions.PromotionSumPresent', on_delete=models.SET_NULL, related_name='offers', verbose_name='Акция №1', null=True, blank=True,
                                              help_text='При покупке от определенной суммы, один товар ценой не больше X в подарок')
    promotion_three_sales = models.ForeignKey('promotions.PromotionThreeSales', on_delete=models.SET_NULL, related_name='offers', verbose_name='Акция №2', null=True, blank=True,
                                              help_text='При покупке на сумму X скидка %, хх - % +, ххх - % ++')
    promotion_min_present = models.ForeignKey('promotions.PromotionMinPresent', on_delete=models.SET_NULL, related_name='offers', verbose_name='Акция №3', null=True, blank=True,
                                              help_text='При покупке N товаров, товар с наименьшей стоимостью в подарок')
    promotion_sale = models.ForeignKey('promotions.PromotionSale', on_delete=models.SET_NULL, related_name='offers', verbose_name='Акция №4', null=True, blank=True,
                                              help_text='Скидка N% на все товары')

    class Meta:
        verbose_name = 'Вариант товара'
        verbose_name_plural = 'Варианты товара'
        unique_together = ('product', 'color', 'size', 'cup')

    def get_image(self):
        return ProductImage.objects.filter(product=self.product, color=self.color).first()

    def get_price(self):
        if self.promotion_sale:
            return self.product.price * (100 - self.promotion_sale.sale) // 100
        return self.product.price

    def __str__(self):
        return '{} - {} - {} - {} - {}'.format(self.product.category, self.product, self.color, self.size, self.cup)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='images', verbose_name='Цвет', null=True, blank=True)

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
                                 processors=[ResizeToFill(150, 130)],
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


class SimilarProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='similars', verbose_name='Товар')
    sim_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Похожий товар')

    class Meta:
        verbose_name = 'Похожий товар'
        verbose_name_plural = 'Похожие товары товара'

    def __str__(self):
        return self.sim_product.name


class FavoriteProduct(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='favorites', verbose_name='Вариант товара')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'
        unique_together = ('offer', 'user')

    def __str__(self):
        return self.user.full_name
