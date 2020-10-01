from django.contrib import admin
from contacts.models import ContactInfo, Social, City, Shop, FeedBack


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'site', 'director')


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'link')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'phone', 'email', 'schedule')


admin.site.register(City)


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_or_phone', 'created')
