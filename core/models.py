from django.db import models


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

    class Meta:
        verbose_name = 'Статические элементы'
        verbose_name_plural = 'Статические элементы'

    def __str__(self):
        return 'Статические элементы №{0}'.format(self.id)
