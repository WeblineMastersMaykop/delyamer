from django.db import models
from django.urls import reverse
from core.models import SEO
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Transpose
from uuid import uuid1


class NewsCategory(models.Model):
    name = models.CharField('Название', max_length=50)

    class Meta:
        verbose_name = 'Категория новости'
        verbose_name_plural = 'Категории новостей'

    def __str__(self):
        return self.name


class News(SEO):
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news', verbose_name='Категория новости')
    title = models.CharField('Название', max_length=250)
    body1 = models.TextField('Текст новости #1', null=True, blank=True)
    body2 = models.TextField('Текст новости #2', null=True, blank=True)
    body3 = models.TextField('Текст новости #3', null=True, blank=True)
    is_active = models.BooleanField('Показывать на сайте', default=True)
    created = models.DateField('Дата создания', auto_now_add=True)
    updated = models.DateField('Дата изменения', auto_now=True)

    image = models.ImageField(upload_to='images/news/', verbose_name='Изображение')

    image_small = ImageSpecField(source='image',
                                 processors=[Transpose('auto'), ResizeToFill(356, 200)],
                                 format='JPEG',
                                 options={'quality': 90})

    image_admin = ImageSpecField(source='image',
                                 processors=[Transpose('auto'), ResizeToFill(70, 40)],
                                 format='JPEG',
                                 options={'quality': 90})

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-created',)

    def __str__(self):
        return self.title


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images', verbose_name='Новость')

    def get_picture_url(self, filename):
        ext = filename.split('.')[-1]
        filename = '{0}.{1}'.format(uuid1(), ext)
        return 'images/news/{0}/{1}'.format(self.news.slug, filename)

    image = models.ImageField(upload_to=get_picture_url, verbose_name='Изображение')

    image_small = ImageSpecField(source='image',
                                 processors=[Transpose('auto'), ResizeToFill(105, 58)],
                                 format='JPEG',
                                 options={'quality': 90})

    image_standart = ImageSpecField(source='image',
                                    processors=[Transpose('auto'), ResizeToFill(729, 410)],
                                    format='JPEG',
                                    options={'quality': 90})

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
