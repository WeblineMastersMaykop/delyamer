from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from products.models import Color, Size, Category, Product, Offer, OfferImage, Property, ProductProperty


admin.site.register(Size)
admin.site.register(Property)


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


class OfferImageInline(admin.TabularInline):
    model = OfferImage
    extra = 0
    classes = ('grp-collapse grp-closed',)


class OfferInline(admin.TabularInline):
    model = Offer
    extra = 0
    classes = ('grp-collapse grp-closed',)


class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty
    extra = 0
    classes = ('grp-collapse grp-closed',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'vendor_code', 'price', 'desc', 'is_new', 'is_bs', 'is_active'),
        }),
        ('SEO', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('slug', 'seo_title', 'seo_desc', 'seo_kwrds'),
        }),
    )

    list_display = ('name', 'category', 'price', 'vendor_code', 'is_new', 'is_bs', 'is_active', 'created', 'updated')
    list_editable = ('is_active', 'is_new', 'is_bs')
    search_fields = ('name', 'vendor_code', 'category__name', 'desc')
    prepopulated_fields = {'slug': ('name',)}
    inlines = (OfferInline, OfferImageInline, ProductPropertyInline)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('product', 'color', 'size', 'stock', 'sale', 'is_active'),
        }),
    )

    list_display = ('product', 'color', 'size', 'stock', 'sale', 'is_active', 'created', 'updated')
    list_editable = ('is_active',)
