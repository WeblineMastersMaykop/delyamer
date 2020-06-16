from django.db import models


class SEO(models.Model):
    seo_title = models.CharField(max_length=250, verbose_name='Title', null=True, blank=True)
    seo_desc = models.CharField(max_length=250, verbose_name='Description', null=True, blank=True)
    seo_kwrds = models.CharField(max_length=250, verbose_name='Keywords', blank=True)
    slug = models.SlugField(max_length=250, verbose_name='Slug', unique=True)

    class Meta:
        abstract = True


class Position(models.Model):
    position = models.PositiveIntegerField(verbose_name='Позиция', null=True, blank=True)

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
    email = models.EmailField(max_length=250, verbose_name='E-mail')

    class Meta:
        verbose_name = 'Кому отправлять письмо'
        verbose_name_plural = 'Кому отправлять письмо'

    def __str__(self):
        return self.email


class MailFromString(models.Model):
    use_tls = models.BooleanField(verbose_name='EMAIL_USE_TLS(gmail.com, mail.ru)')
    use_ssl = models.BooleanField(verbose_name='EMAIL_USE_SSL(yandex.ru)')
    port = models.PositiveIntegerField(verbose_name='EMAIL_PORT')
    host = models.CharField(max_length=250, verbose_name='EMAIL_HOST')
    host_user = models.EmailField(max_length=250, verbose_name='EMAIL_HOST_USER')
    host_password = models.CharField(max_length=250, verbose_name='EMAIL_HOST_PASSWORD')

    class Meta:
        verbose_name = 'Откуда отправлять письмо'
        verbose_name_plural = 'Откуда отправлять письмо'

    def __str__(self):
        return self.host_user


class TitleTag(models.Model):
    url = models.CharField(max_length=250, verbose_name='URL')
    seo_title = models.CharField(max_length=250, verbose_name='Title', null=True, blank=True)
    seo_desc = models.CharField(max_length=250, verbose_name='Description', null=True, blank=True)
    seo_kwrds = models.CharField(max_length=250, verbose_name='Keywords', null=True, blank=True)

    class Meta:
        verbose_name = 'SEO title'
        verbose_name_plural = 'SEO titles'

    def __str__(self):
        return self.seo_title


class Index(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    title_text = models.TextField(verbose_name='Текст под заголовком')
    about = models.TextField(verbose_name='О нас')

    class Meta:
        verbose_name = 'Статические элементы'
        verbose_name_plural = 'Статические элементы'

    def __str__(self):
        return 'Статические элементы №{0}'.format(self.id)
