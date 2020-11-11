from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class DeliveryMethod(models.Model):
    DELIVERY_CHOICES = (
        ('pochta', 'Почта России'),
    )

    name = models.CharField(max_length=100, choices=DELIVERY_CHOICES, verbose_name='Тип доставки', default='pochta')
    info = models.CharField('Доп. информация', max_length=100, null=True, blank=True)
    price = models.PositiveIntegerField('Цена')

    class Meta:
        verbose_name = 'Цена доставки'
        verbose_name_plural = 'Цены на доставку'

    def __str__(self):
        return self.get_name_display()


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('paiding', 'Оплачивается'),
        ('paid', 'Оплачен'),
        ('error', 'Ошибка оплаты'),
        ('canceled', 'Отменен'),
        ('shipped', 'Отгружен'),
        ('finished', 'Завершён'),
    )

    PAY_CHOICES = (
        ('credit', 'Кредит'),
        ('online', 'Онлайн'),
    )

    DELIVERY_CHOICES = (
        ('cdek_point', 'СДЭК (пункт выдачи)'),
        ('cdek_home', 'СДЭК (курьером до двери)'),
        ('pochta', 'Почта России'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='orders', verbose_name='Пользователь', null=True, blank=True)
    full_name = models.CharField('ФИО', max_length=250)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Электронная почта', null=True, blank=True)
    # postcode = models.CharField('Почтовый индекс', max_length=10, null=True, blank=True)
    country = models.CharField('Страна', max_length=100, null=True, blank=True)
    region = models.CharField('Регион', max_length=100, null=True, blank=True)
    city = models.CharField('Населенный пункт', max_length=100, null=True, blank=True)
    micro_district = models.CharField('Микрорайон', max_length=100, null=True, blank=True)
    street = models.CharField('Улица', max_length=100, null=True, blank=True)
    house_nmb = models.CharField('Номер дома', max_length=20, null=True, blank=True)
    building_nmb = models.CharField('Корпус', max_length=20, null=True, blank=True)
    room_nmb = models.CharField('Квартира/Офис', max_length=20, null=True, blank=True)

    total_price = models.PositiveIntegerField('Итоговая стоимость', default=0)
    total_price_with_sale = models.PositiveIntegerField('Итоговая стоимость со скидкой', default=0)
    delivery = models.CharField(max_length=100, choices=DELIVERY_CHOICES, verbose_name='Тип доставки', default='cdek', null=True, blank=True)
    delivery_price = models.PositiveIntegerField(verbose_name='Сумма доставки', null=True, blank=True)
    track_number = models.CharField(max_length=50, verbose_name='Трек номер', null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, verbose_name='Статус', default='new')
    pay_type = models.CharField(max_length=100, choices=PAY_CHOICES, verbose_name='Способ оплаты', null=True, blank=True)
    sync_1c = models.BooleanField('Выгружено в 1С', default=False)

    created = models.DateTimeField('Создано', auto_now_add=True)
    updated = models.DateTimeField('Изменено', auto_now=True)

    def get_absolute_url(self):
        return reverse('order_detail', args=[self.id])

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Список заказов'
        ordering = ('-created',)

    def __str__(self):
        return 'Заказ №{}'.format(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    offer = models.ForeignKey('products.Offer', on_delete=models.CASCADE, verbose_name='Товар')
    price = models.PositiveIntegerField('Цена')
    quantity = models.PositiveIntegerField('Количество', default=1)
    discount = models.PositiveIntegerField('Сумма скидки', default=0)
    total_price_with_sale = models.PositiveIntegerField('Итоговая сумма по строке')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return '{} -- Заказ №{}'.format(self.offer, self.order.id)


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
