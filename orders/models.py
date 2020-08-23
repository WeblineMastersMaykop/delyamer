from django.db import models
from django.conf import settings


class DeliveryMethod(models.Model):
    name = models.CharField('Название', max_length=100)
    info = models.CharField('Доп. информация', max_length=100, null=True, blank=True)
    price = models.PositiveIntegerField('Цена', null=True, blank=True)

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы доставки'

    def __str__(self):
        return '{}{}'.format(self.name, ' -- ' + self.info if self.info else '')


class OrderStatus(models.Model):
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='orders', verbose_name='Пользователь', null=True, blank=True)
    full_name = models.CharField('ФИО', max_length=250)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Электронная почта', null=True, blank=True)
    postcode = models.CharField('Почтовый индекс', max_length=10, null=True, blank=True)
    country = models.CharField('Страна', max_length=100, null=True, blank=True)
    region = models.CharField('Регион', max_length=100, null=True, blank=True)
    city = models.CharField('Населенный пункт', max_length=100, null=True, blank=True)
    address = models.CharField('Адрес', max_length=250, null=True, blank=True)

    # total_price = models.PositiveIntegerField('Итоговая стоимость', default=0)
    delivery = models.ForeignKey(DeliveryMethod, on_delete=models.SET_NULL, related_name='orders', verbose_name='Способ доставки', null=True, blank=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, related_name='orders', verbose_name='Статус заказа', null=True, blank=True)

    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Изменено', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Список заказов'

    def __str__(self):
        return 'Заказ №{}'.format(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    offer = models.ForeignKey('products.Offer', on_delete=models.CASCADE, verbose_name='Товар')
    price = models.PositiveIntegerField('Цена')
    quantity = models.PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return '{} -- Заказ №{}'.format(self.offer.name, self.order.id)

    def get_cost(self):
        return self.price * self.quantity
