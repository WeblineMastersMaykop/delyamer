from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.html import mark_safe


class User(AbstractUser):
    full_name = models.CharField('ФИО', max_length=250, null=True, blank=True)
    # postcode = models.CharField('Почтовый индекс', max_length=10, null=True, blank=True)
    country = models.CharField('Страна', max_length=100, null=True, blank=True)
    region = models.CharField('Область/Регион', max_length=100, null=True, blank=True)
    city = models.CharField('Населенный пункт', max_length=100, null=True, blank=True)
    micro_district = models.CharField('Микрорайон', max_length=100, null=True, blank=True)
    street = models.CharField('Улица', max_length=100, null=True, blank=True)
    house_nmb = models.CharField('Номер дома', max_length=20, null=True, blank=True)
    building_nmb = models.CharField('Корпус', max_length=20, null=True, blank=True)
    room_nmb = models.CharField('Квартира/Офис', max_length=20, null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20, null=True, blank=True)
    new_email = models.EmailField('Временная эл. почта', max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'Все пользователи'
        verbose_name_plural = 'Все пользователи'

    def get_active_orders(self):
        return self.orders.all().exclude(status='finished')

    def get_finished_orders(self):
        return self.orders.filter(status='finished')

    def get_favorites_offers(self):
        return [favorite.offer.id for favorite in self.favorites.select_related('offer').all()]

class UserGroup(Group):
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
