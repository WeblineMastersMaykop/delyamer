from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Transpose


class ContactInfo(models.Model):
    name = models.CharField('Наименование организации', max_length=250)
    address = models.CharField('Адрес', max_length=250)
    inn = models.CharField('ИНН', max_length=20)
    kpp = models.CharField('КПП', max_length=20)
    bik = models.CharField('БИК', max_length=20)
    cor_acc = models.CharField('Кор. счет', max_length=30)
    check_acc = models.CharField('Рас. счет', max_length=30)
    bank = models.CharField('Банк получателя', max_length=100)
    okpo = models.CharField('ОКПО', max_length=20)
    okohn = models.CharField('ОКОХН', max_length=20)
    ogrn = models.CharField('ОГРН', max_length=20)
    email = models.EmailField('Эл. почта', max_length=100)
    site = models.CharField('Сайт', max_length=50)
    phone = models.CharField('Телефон', max_length=20)
    director = models.CharField('Директор', max_length=50)

    class Meta:
        verbose_name = 'Контакты или реквизиты'
        verbose_name_plural = 'Контакты и реквизиты'

    def __str__(self):
        return self.name


class Social(models.Model):
    name = models.CharField('Название социальной сети', max_length=50)
    short_name = models.CharField('Название для Font Awesome', max_length=20)
    link = models.CharField('Ссылка или номер', max_length=50)

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField('Название города', max_length=50)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class Shop(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='shops', verbose_name='Город')
    address = models.CharField('Адрес', max_length=250)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Эл. почта', max_length=100, null=True, blank=True)
    schedule = models.CharField('Режим работы', max_length=250, help_text='Пункты разделять ";"')
    map_code = models.TextField('Скрипт карты')

    image = models.ImageField(upload_to='images/shops/', verbose_name='Изображение')

    image_small = ImageSpecField(source='image',
                                processors=[Transpose('auto'), ResizeToFill(600, 257)],
                                format='JPEG',
                                options={'quality': 90})

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.address


class FeedBack(models.Model):
    name = models.CharField(max_length=250, verbose_name='Имя')
    email_or_phone = models.CharField(max_length=250, verbose_name='E-mail или телефон')
    text = models.TextField(verbose_name='Текст сообщения')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время заявки')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.email_or_phone)
