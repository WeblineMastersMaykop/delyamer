from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class SEO(models.Model):
    seo_title = models.CharField('Title', max_length=250, null=True, blank=True)
    seo_desc = models.CharField('Description', max_length=250, null=True, blank=True)
    seo_kwrds = models.CharField('Keywords', max_length=250, blank=True)
    slug = models.SlugField('Slug', max_length=250, unique=True)

    class Meta:
        abstract = True


class Position(models.Model):
    position = models.PositiveIntegerField('Позиция', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.position is None:
            try:
                last = self.objects.order_by('-position')[0]
                self.position = last.position + 1
            except:
                self.position = 0
        return super(Position, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ('position',)


class MailToString(models.Model):
    # EMAIL_TYPES = [
    #     ('req', 'Для заявок'),
    #     ('all', 'Для остального'),
    # ]

    # email_type = models.CharField(max_length=250, choices=EMAIL_TYPES, verbose_name='Тип email')
    email = models.EmailField('E-mail', max_length=250)

    class Meta:
        verbose_name = 'Кому отправлять письмо'
        verbose_name_plural = 'Кому отправлять письмо'

    def __str__(self):
        return self.email


class MailFromString(models.Model):
    use_tls = models.BooleanField('EMAIL_USE_TLS(gmail.com, mail.ru)')
    use_ssl = models.BooleanField('EMAIL_USE_SSL(yandex.ru)')
    port = models.PositiveIntegerField('EMAIL_PORT')
    host = models.CharField('EMAIL_HOST', max_length=250)
    host_user = models.EmailField('EMAIL_HOST_USER', max_length=250)
    host_password = models.CharField('EMAIL_HOST_PASSWORD', max_length=250)

    class Meta:
        verbose_name = 'Откуда отправлять письмо'
        verbose_name_plural = 'Откуда отправлять письмо'

    def __str__(self):
        return self.host_user


class TitleTag(models.Model):
    url = models.CharField('URL', max_length=250)
    seo_title = models.CharField('Title', max_length=250)
    seo_desc = models.CharField('Description', max_length=250, null=True, blank=True)
    seo_kwrds = models.CharField('Keywords', max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'SEO title'
        verbose_name_plural = 'SEO titles'

    def __str__(self):
        return self.seo_title


class Index(models.Model):
    phone = models.CharField('Телефон в шапке сайта', max_length=20)
    banner = models.ForeignKey('Banner', on_delete=models.SET_NULL, verbose_name='Баннер', null=True, blank=True)

    class Meta:
        verbose_name = 'Статические элементы'
        verbose_name_plural = 'Статические элементы'

    def __str__(self):
        return 'Статические элементы №{0}'.format(self.id)


class Slide(models.Model):
    main_text = models.CharField('Заголовок', max_length=250, null=True, blank=True)
    sub_text = models.CharField('Описание', max_length=250, null=True, blank=True)
    url = models.CharField('Ссылка', max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='images/slides/', verbose_name='Изображение', null=True, blank=True)
    image_big = ImageSpecField(source='image',
                                 processors=[ResizeToFill(1116, 480)],
                                 format='JPEG',
                                 options={'quality': 90})

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

    def __str__(self):
        return 'Слайд №{}'.format(self.id)


class Banner(models.Model):
    main_text = models.CharField('Заголовок', max_length=250)
    sub_text = models.TextField('Описание')
    url = models.CharField('Ссылка', max_length=250)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return 'Баннер №{}'.format(self.id)