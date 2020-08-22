from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.html import mark_safe


class User(AbstractUser):
    full_name = models.CharField('ФИО', max_length=250, null=True, blank=True)
    postcode = models.CharField('Почтовый индекс', max_length=10, null=True, blank=True)
    country = models.CharField('Страна', max_length=100, null=True, blank=True)
    region = models.CharField('Регион', max_length=100, null=True, blank=True)
    city = models.CharField('Населенный пункт', max_length=100, null=True, blank=True)
    address = models.CharField('Адрес', max_length=250, null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = 'Все пользователи'
        verbose_name_plural = 'Все пользователи'


class UserGroup(Group):
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
