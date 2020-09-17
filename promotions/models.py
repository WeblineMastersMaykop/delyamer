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
    text = models.CharField('Текст акции', max_length=100)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'От X руб. товар не больше Y в подарок'
        unique_together = ('total_price', 'price')

    def __str__(self):
        return 'От {} руб. товар не больше {} руб. в подарок'.format(self.total_price, self.price)


class PromotionThreeSales(models.Model):
    price1 = models.PositiveIntegerField('Сумма 1')
    sale1 = models.PositiveIntegerField('Скидка 1')
    price2 = models.PositiveIntegerField('Сумма 2')
    sale2 = models.PositiveIntegerField('Скидка 2')
    price3 = models.PositiveIntegerField('Сумма 3')
    sale3 = models.PositiveIntegerField('Скидка 3')
    text = models.CharField('Текст акции', max_length=100)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'От X руб. скидка %, XX - %, XXX - %'

    def __str__(self):
        return '{} руб. - {}; {} руб. - {}; {} руб. - {}'.format(
                    self.price1, self.sale1,
                    self.price2, self.sale2,
                    self.price3, self.sale3,
                )


class PromotionMinPresent(models.Model):
    nmb = models.PositiveIntegerField('Количество товаров')
    text = models.CharField('Текст акции', max_length=100)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акция N + 1'

    def __str__(self):
        return 'Акция {} + 1'.format(self.nmb)


class PromotionSale(models.Model):
    sale = models.PositiveIntegerField('Скидка')
    text = models.CharField('Текст акции', max_length=100)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Скидка N%'

    def __str__(self):
        return 'Скидка {}'.format(self.sale)
