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
    new_email = models.EmailField('Временная эл. почта', max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'Все пользователи'
        verbose_name_plural = 'Все пользователи'

    def get_active_orders(self):
        return self.orders.all().exclude(status='finished').select_related('delivery')

    def get_finished_orders(self):
        return self.orders.filter(status='finished').select_related('delivery')

    def get_favorites_offers(self):
        return [favorive.offer.id for favorite in self.favorites.select_related('offer').all()]

class UserGroup(Group):
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
