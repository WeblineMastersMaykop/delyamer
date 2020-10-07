from django.contrib import admin
from users.models import User, UserGroup
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext, gettext_lazy as _


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('full_name', 'phone', 'email', 'postcode', 'country', 'region', 'city',
            'micro_district', 'street', 'house_nmb', 'building_nmb', 'room_nmb'),
        }),
        (_('Permissions'), {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('last_login', 'date_joined'),
        }),
    )

    list_display = ('username', 'full_name', 'phone', 'is_active', 'is_staff')
    search_fields = ('username', 'full_name', 'phone')

admin.site.unregister(Group)

@admin.register(UserGroup)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)
