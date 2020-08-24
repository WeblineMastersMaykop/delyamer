from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Promotion(models.Model):
    PROMOTION_TYPES = (
        ('type1', 'При покупке от определенной суммы, один товар ценой не больше X в подарок'),
        ('type2', 'При покупке на сумму X скидка %, хх - % +, ххх - % ++'),
        ('type3', 'При покупке N товаров, товар с наименьшей стоимостью в подарок'),
        ('type4', 'Скидка N% на все товары'),
    )

    promotion_type = models.CharField(max_length=250, choices=PROMOTION_TYPES, verbose_name='Тип акции')
    main_text = models.TextField('Заголовок', max_length=250, null=True, blank=True)
    sub_text = models.TextField('Описание', max_length=250, null=True, blank=True)
    url = models.URLField('Ссылка', null=True, blank=True)
    image = models.ImageField(upload_to='images/promotions/', verbose_name='Изображение', null=True, blank=True)

    type1_sum = models.PositiveIntegerField('При покупке от суммы', null=True, blank=True)
    type1_price = models.PositiveIntegerField('В подарок не больше', null=True, blank=True)

    type2_price1 = models.PositiveIntegerField('Сумма 1', null=True, blank=True)
    type2_sale1 = models.PositiveIntegerField('Скидка 1', null=True, blank=True)
    type2_price2 = models.PositiveIntegerField('Сумма 2', null=True, blank=True)
    type2_sale2 = models.PositiveIntegerField('Скидка 2', null=True, blank=True)
    type2_price3 = models.PositiveIntegerField('Сумма 3', null=True, blank=True)
    type2_sale3 = models.PositiveIntegerField('Скидка 3', null=True, blank=True)

    type3_nmb = models.PositiveIntegerField('При покупке N товаров', null=True, blank=True)

    type4_sale = models.PositiveIntegerField('Скидка', null=True, blank=True)

    image_big = ImageSpecField(source='image',
                                 processors=[ResizeToFill(1116, 480)],
                                 format='JPEG',
                                 options={'quality': 90})

    products = models.ManyToManyField('products.Offer', related_name='promotions', verbose_name='Товары', blank=True)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return self.main_text


class PromoCode(models.Model):
    code = models.CharField('Промокод', max_length=30)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code