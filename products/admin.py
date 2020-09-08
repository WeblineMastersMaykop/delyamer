from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from products.models import Color, Size, Category, Product, Offer, ProductImage, Cup


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'code_1c', 'image'),
        }),
        ('SEO', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('slug', 'seo_title', 'seo_desc', 'seo_kwrds'),
        }),
    )

    list_display = ('name', 'code_1c', 'position')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'code_1c')


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Cup)
class CupAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    classes = ('grp-collapse grp-closed',)


class OfferInline(admin.StackedInline):
    model = Offer
    extra = 0
    classes = ('grp-collapse grp-closed',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('category', 'code_1c', 'name', 'vendor_code', 'pushup', 'price', 'desc', 'is_new', 'is_bs', 'is_active'),
        }),
        ('SEO', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('slug', 'seo_title', 'seo_desc', 'seo_kwrds'),
        }),
    )

    list_display = ('name', 'category', 'code_1c', 'price', 'vendor_code', 'pushup', 'is_new', 'is_bs', 'is_active', 'created', 'updated')
    list_editable = ('is_active', 'is_new', 'is_bs')
    search_fields = ('name', 'code_1c', 'vendor_code', 'category__name')
    list_filter = ('is_active', 'is_new', 'is_bs', 'category', 'pushup')
    prepopulated_fields = {'slug': ('name','code_1c')}
    inlines = (OfferInline, ProductImageInline)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('product', 'color', 'size', 'cup', 'stock', 'is_active'),
        }),
        ('Акции', {
            'fields': ('promotion_sum_present', 'promotion_three_sales', 'promotion_min_present', 'promotion_sale'),
        })
    )

    list_display = ('product', 'color', 'size', 'cup', 'stock', 'is_active', 'created', 'updated')
    list_editable = ('is_active',)
    search_fields = ('product__name', 'color__name', 'size__name', 'cup__name', 'product__category__name')
