from django.db import models
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from django.core.exceptions import ValidationError
# from django.db.utils import IntegrityError
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from products.models import Offer, Color, Size, Cup, Product, Category


# class Promotion(models.Model):
#     PROMOTION_TYPES = (
#         ('type1', 'При покупке от определенной суммы, один товар ценой не больше X в подарок'),
#         ('type2', 'При покупке на сумму X скидка %, хх - % +, ххх - % ++'),
#         ('type3', 'При покупке N товаров, товар с наименьшей стоимостью в подарок'),
#         ('type4', 'Скидка N% на все товары'),
#     )

#     promotion_type = models.CharField(max_length=250, choices=PROMOTION_TYPES, verbose_name='Тип акции')
#     main_text = models.TextField('Заголовок', max_length=250, null=True, blank=True)
#     sub_text = models.TextField('Описание', max_length=250, null=True, blank=True)
#     url = models.URLField('Ссылка', null=True, blank=True)
#     image = models.ImageField(upload_to='images/promotions/', verbose_name='Изображение', null=True, blank=True)

#     type1_sum = models.PositiveIntegerField('При покупке от суммы', null=True, blank=True)
#     type1_price = models.PositiveIntegerField('В подарок не больше', null=True, blank=True)

#     type2_price1 = models.PositiveIntegerField('Сумма 1', null=True, blank=True)
#     type2_sale1 = models.PositiveIntegerField('Скидка 1', null=True, blank=True)
#     type2_price2 = models.PositiveIntegerField('Сумма 2', null=True, blank=True)
#     type2_sale2 = models.PositiveIntegerField('Скидка 2', null=True, blank=True)
#     type2_price3 = models.PositiveIntegerField('Сумма 3', null=True, blank=True)
#     type2_sale3 = models.PositiveIntegerField('Скидка 3', null=True, blank=True)

#     type3_nmb = models.PositiveIntegerField('При покупке N товаров', null=True, blank=True)

#     type4_sale = models.PositiveIntegerField('Скидка', null=True, blank=True)

#     image_big = ImageSpecField(source='image',
#                                  processors=[ResizeToFill(1116, 480)],
#                                  format='JPEG',
#                                  options={'quality': 90})

#     offers = models.ManyToManyField(Offer, related_name='promotions', verbose_name='Варианты товара', blank=True)

#     class Meta:
#         verbose_name = 'Акция'
#         verbose_name_plural = 'Акции'

#     def __str__(self):
#         return self.main_text


# @receiver(m2m_changed, sender=Promotion.offers.through)
# def verify_uniqueness(sender, **kwargs):
#     promotion = kwargs.get('instance', None)
#     action = kwargs.get('action', None)
#     offers = kwargs.get('pk_set', None)

#     if action == 'pre_add':
#         for offer in offers:
#             if Promotion.objects.filter(promotion_type=promotion.promotion_type).filter(offers=offer):
#                 raise IntegrityError('Вариант товара {} уже учавствует в подобной акции'.format(Offer.objects.get(pk=offer)))


class PromoCode(models.Model):
    code = models.CharField('Промокод', max_length=30)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code


class Promotion(models.Model):
    main_text = models.TextField('Заголовок', max_length=250, null=True, blank=True)
    sub_text = models.TextField('Описание', max_length=250, null=True, blank=True)
    url = models.URLField('Ссылка', null=True, blank=True)
    image = models.ImageField(upload_to='images/promotions/', verbose_name='Изображение', null=True, blank=True)
    image_big = ImageSpecField(source='image',
                                 processors=[ResizeToFill(1116, 480)],
                                 format='JPEG',
                                 options={'quality': 90})

    class Meta:
        abstract = True


class PromotionSumPresent(Promotion):
    offer_sum = models.PositiveIntegerField('При покупке от суммы')
    price = models.PositiveIntegerField('В подарок не больше')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'При покупке от определенной суммы, один товар ценой не больше X в подарок'
        unique_together = ('offer_sum', 'price')

    def __str__(self):
        return 'При покупке от {} руб. один товар ценой не больше {} руб. в подарок'.format(self.offer_sum, self.price)


class PromotionThreeSales(Promotion):
    price1 = models.PositiveIntegerField('Сумма 1')
    sale1 = models.PositiveIntegerField('Скидка 1')
    price2 = models.PositiveIntegerField('Сумма 2')
    sale2 = models.PositiveIntegerField('Скидка 2')
    price3 = models.PositiveIntegerField('Сумма 3')
    sale3 = models.PositiveIntegerField('Скидка 3')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'При покупке на сумму X скидка %, хх - % +, ххх - % ++'

    def __str__(self):
        return 'При покупке на сумму {} руб. скидка {}%; {} руб. - {}%; {} руб. - {}%'.format(
                    self.price1, self.sale1,
                    self.price2, self.sale2,
                    self.price3, self.sale3,
                )


class PromotionMinPresent(Promotion):
    nmb = models.PositiveIntegerField('Количество товаров')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'При покупке N товаров, товар с наименьшей стоимостью в подарок'

    def __str__(self):
        return 'При покупке {} товаров, товар с наименьшей стоимостью в подарок'.format(self.nmb)


class PromotionSale(Promotion):
    sale = models.PositiveIntegerField('Скидка')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Скидка N% на все товары'

    def __str__(self):
        return 'Скидка {}% на все товары'.format(self.sale)


# class PromotionEdit(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='prom_edits', verbose_name='Категория', null=True, blank=True)
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='prom_edits', verbose_name='Товар', null=True, blank=True)
#     offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, related_name='prom_edits', verbose_name='Вариант товара', null=True, blank=True)
#     color = models.ForeignKey(Color, on_delete=models.SET_NULL, related_name='prom_edits', verbose_name='Цвет', null=True, blank=True)
#     cup = models.ForeignKey(Cup, on_delete=models.SET_NULL, related_name='prom_edits', verbose_name='Чашка', null=True, blank=True)
#     size = models.ForeignKey(Size, on_delete=models.SET_NULL, related_name='prom_edits', verbose_name='Размер', null=True, blank=True)
#     size = models.ForeignKey(Size, on_delete=models.SET_NULL, related_name='prom_edits', verbose_name='Размер', null=True, blank=True)

#     class Meta:
#         verbose_name = 'Связь между акциями и Вариантами товара'
#         verbose_name_plural = 'Управление акциями'

#     def __str__(self):
#         return 'Связь {}'.format(self.id)