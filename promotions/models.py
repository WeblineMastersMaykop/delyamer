from django.db import models
from products.models import Offer, Color, Size, Cup, Product, Category


class PromoCode(models.Model):
    code = models.CharField('Промокод', max_length=30, unique=True)
    sale = models.PositiveIntegerField('Скидка', default=0)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code


class PromotionSumPresent(models.Model):
    total_price = models.PositiveIntegerField('При покупке от суммы')
    price = models.PositiveIntegerField('В подарок не больше')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'При покупке от определенной суммы, один товар ценой не больше X в подарок'
        unique_together = ('total_price', 'price')

    def __str__(self):
        return 'При покупке от {} руб. один товар ценой не больше {} руб. в подарок'.format(self.total_price, self.price)


class PromotionThreeSales(models.Model):
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


class PromotionMinPresent(models.Model):
    nmb = models.PositiveIntegerField('Количество товаров')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'При покупке N товаров, товар с наименьшей стоимостью в подарок'

    def __str__(self):
        return 'При покупке {} товаров, товар с наименьшей стоимостью в подарок'.format(self.nmb)


class PromotionSale(models.Model):
    sale = models.PositiveIntegerField('Скидка')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Скидка N% на все товары'

    def __str__(self):
        return 'Скидка {}% на все товары'.format(self.sale)
