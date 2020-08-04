from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from products.models import Color, Size, Category, Product


admin.site.register(Size)


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    fieldsets = (
        (None, {
            'fields': ('parent', 'name'),
        }),
        ('SEO', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('slug', 'seo_title', 'seo_desc', 'seo_kwrds'),
        }),
    )

    list_display = ('name', 'parent', 'position')
    sortable_field_name = 'position'
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'price', 'sale', 'is_new', 'is_bs', 'is_active'),
        }),
        ('SEO', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('slug', 'seo_title', 'seo_desc', 'seo_kwrds'),
        }),
    )

    list_display = ('name', 'category', 'price', 'sale', 'is_new', 'is_bs', 'is_active', 'created', 'updated')
    list_editable = ('is_active', 'is_new', 'is_bs')
    prepopulated_fields = {'slug': ('name',)}