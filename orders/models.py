from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class DeliveryMethod(models.Model):
    name = models.CharField('Название', max_length=100)
    info = models.CharField('Доп. информация', max_length=100, null=True, blank=True)
    price = models.PositiveIntegerField('Цена', null=True, blank=True)

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы доставки'

    def __str__(self):
        return '{}{}'.format(self.name, ' -- ' + self.info if self.info else '')


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('shops', 'Магазины'),
        ('products', 'Каталог'),
        ('news', 'Новости'),
        ('contacts', 'Контакты'),
        ('finished', 'Завершён'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', verbose_name='Пользователь', null=True, blank=True)
    full_name = models.CharField('ФИО', max_length=250)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Электронная почта', null=True, blank=True)
    postcode = models.CharField('Почтовый индекс', max_length=10, null=True, blank=True)
    country = models.CharField('Страна', max_length=100, null=True, blank=True)
    region = models.CharField('Регион', max_length=100, null=True, blank=True)
    city = models.CharField('Населенный пункт', max_length=100, null=True, blank=True)
    address = models.CharField('Адрес', max_length=250, null=True, blank=True)

    total_price = models.PositiveIntegerField('Итоговая стоимость', default=0)
    delivery = models.ForeignKey(DeliveryMethod, on_delete=models.SET_NULL, related_name='orders', verbose_name='Способ доставки', null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, verbose_name='Статус', default='new')

    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Изменено', auto_now=True)

    def get_absolute_url(self):
        return reverse('order_detail', args=[self.id])

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Список заказов'
        ordering = ('updated',)

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
        return '{} -- Заказ №{}'.format(self.offer, self.order.id)

    def get_cost(self):
        return self.price * self.quantity


class Review(models.Model):
    RATING_CHOICES = (
        ('one', '1'),
        ('two', '2'),
        ('three', '3'),
        ('four', '4'),
        ('five', '5'),
    )

    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name='review', verbose_name='Товар в заказе')
    rating = models.CharField(max_length=20, choices=RATING_CHOICES, verbose_name='Рейтинг', default='one')
    text = models.TextField('Текст')
    created = models.DateField('Дата создания', auto_now_add=True)
    updated = models.DateField('Дата изменения', auto_now=True)


    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return '{} -- {}'.format(self.order_item.offer, self.order_item.order.user.username)
