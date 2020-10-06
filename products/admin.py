from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from products.models import Color, Size, Category, Product, Offer, ProductImage, Cup, SimilarProduct, FavoriteProduct
from promotions.models import PromotionMinPresent, PromotionSale, PromotionSumPresent, PromotionThreeSales


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

    def get_actions(self, request):
        actions = super().get_actions(request)

        def func_maker(pr=None, pr_type=None):
            def func(self, request, queryset):
                if pr_type == 'promotion_sum_present':
                    Offer.objects.select_related('product', 'product__category').filter(product__category__in=queryset).update(
                        promotion_sum_present=pr, promotion_three_sales=None, promotion_min_present=None, promotion_sale=None
                    )
                elif pr_type == 'promotion_three_sales':
                    Offer.objects.select_related('product', 'product__category').filter(product__category__in=queryset).update(
                        promotion_sum_present=None, promotion_three_sales=pr, promotion_min_present=None, promotion_sale=None
                    )
                elif pr_type == 'promotion_min_present':
                    Offer.objects.select_related('product', 'product__category').filter(product__category__in=queryset).update(
                        promotion_sum_present=None, promotion_three_sales=None, promotion_min_present=pr, promotion_sale=None
                    )
                elif pr_type == 'promotion_sale':
                    Offer.objects.select_related('product', 'product__category').filter(product__category__in=queryset).update(
                        promotion_sum_present=None, promotion_three_sales=None, promotion_min_present=None, promotion_sale=pr
                    )
                else:
                    Offer.objects.select_related('product', 'product__category').filter(product__category__in=queryset).update(
                        promotion_sum_present=None, promotion_three_sales=None, promotion_min_present=None, promotion_sale=None
                    )
            return func

        for pr in PromotionSumPresent.objects.all():
            func = func_maker(pr, 'promotion_sum_present')
            text = 'sum_present_{}'.format(pr.id)
            actions[text] = (func, text, str(pr))

        for pr in PromotionThreeSales.objects.all():
            func = func_maker(pr, 'promotion_three_sales')
            text = 'three_sales_{}'.format(pr.id)
            actions[text] = (func, text, str(pr))

        for pr in PromotionMinPresent.objects.all():
            func = func_maker(pr, 'promotion_min_present')
            text = 'min_present_{}'.format(pr.id)
            actions[text] = (func, text, str(pr))

        for pr in PromotionSale.objects.all():
            func = func_maker(pr, 'promotion_sale')
            text = 'sale_{}'.format(pr.id)
            actions[text] = (func, text, str(pr))

        actions['delete_pr'] = (func_maker(), 'delete_pr', 'Убрать акции у товаров')

        return actions


@admin.register(Color)
class ColorAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'color', 'is_multi', 'code_1c', 'position')
    list_editable = ('is_multi',)


@admin.register(Size)
class SizeAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'position')


@admin.register(Cup)
class CupAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'position')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    classes = ('grp-collapse grp-closed',)


class OfferInline(admin.StackedInline):
    model = Offer
    extra = 0
    classes = ('grp-collapse grp-closed',)


class SimilarProductInline(admin.TabularInline):
    model = SimilarProduct
    fk_name = 'product'
    extra = 0
    autocomplete_fields = ('sim_product',)
    classes = ('grp-collapse grp-closed',)


class FavoriteProductInline(admin.TabularInline):
    model = FavoriteProduct
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
    list_editable = ('is_active', 'is_new', 'is_bs', 'pushup')
    search_fields = ('name', 'code_1c', 'vendor_code', 'category__name')
    list_filter = ('is_active', 'is_new', 'is_bs', 'category', 'pushup')
    prepopulated_fields = {'slug': ('name','code_1c')}
    inlines = (OfferInline, ProductImageInline, SimilarProductInline)

    def get_actions(self, request):
        actions = super().get_actions(request)

        def func_maker(pr=None, pr_type=None):
            def func(self, request, queryset):
                if pr_type == 'promotion_sum_present':
                    Offer.objects.filter(product__in=queryset).update(
                        promotion_sum_present=pr, promotion_three_sales=None, promotion_min_present=None, promotion_sale=None
                    )
                elif pr_type == 'promotion_three_sales':
                    Offer.objects.filter(product__in=queryset).update(
                        promotion_sum_present=None, promotion_three_sales=pr, promotion_min_present=None, promotion_sale=None
                    )
                elif pr_type == 'promotion_min_present':
                    Offer.objects.filter(product__in=queryset).update(
                        promotion_sum_present=None, promotion_three_sales=None, promotion_min_present=pr, promotion_sale=None
                    )
                elif pr_type == 'promotion_sale':
                    Offer.objects.filter(product__in=queryset).update(
                        promotion_sum_present=None, promotion_three_sales=None, promotion_min_present=None, promotion_sale=pr
                    )
                else:
                    Offer.objects.filter(product__in=queryset).update(
                        promotion_sum_present=None, promotion_three_sales=None, promotion_min_present=None, promotion_sale=None
                    )
            return func

        for pr in PromotionSumPresent.objects.all():
            func = func_maker(pr, 'promotion_sum_present')
            text = 'sum_present_{}'.format(pr.id)
            actions[text] = (func, text, str(pr))

        for pr in PromotionThreeSales.objects.all():
            func = func_maker(pr, 'promotion_three_sales')
            text = 'three_sales_{}'.format(pr.id)
            actions[text] = (func, text, str(pr))

        for pr in PromotionMinPresent.objects.all():
            func = func_maker(pr, 'promotion_min_present')
            text = 'min_present_{}'.format(pr.id)
            actions[text] = (func, text, str(pr))

        for pr in PromotionSale.objects.all():
            func = func_maker(pr, 'promotion_sale')
            text = 'sale_{}'.format(pr.id)
            actions[text] = (func, text, str(pr))

        actions['delete_pr'] = (func_maker(), 'delete_pr', 'Убрать акции у товаров')

        return actions


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

    list_display = ('product', 'color', 'size', 'cup', 'stock', 'is_active', 'created', 'updated',
                    'promotion_sum_present', 'promotion_three_sales', 'promotion_min_present', 'promotion_sale')
    list_editable = ('is_active',)
    search_fields = ('product__name', 'color__name', 'size__name', 'cup__name', 'product__category__name')
    list_filter = ('color', 'size', 'cup', 'product__category', 'is_active')
    inlines = (FavoriteProductInline,)

    def get_actions(self, request):
        actions = super().get_actions(request)

        def func_maker(pr=None, pr_type=None):
            def func(self, request, queryset):
                if pr_type == 'promotion_sum_present':
                    queryset.update(promotion_sum_present=pr, promotion_three_sales=None, promotion_min_present=None, promotion_sale=None)
                elif pr_type == 'promotion_three_sales':
                    queryset.update(promotion_sum_present=None, promotion_three_sales=pr, promotion_min_present=None, promotion_sale=None)
                elif pr_type == 'promotion_min_present':
                    queryset.update(promotion_sum_present=None, promotion_three_sales=None, promotion_min_present=pr, promotion_sale=None)
                elif pr_type == 'promotion_sale':
                    queryset.update(promotion_sum_present=None, promotion_three_sales=None, promotion_min_present=None, promotion_sale=pr)
                else:
                    queryset.update(promotion_sum_present=None, promotion_three_sales=None, promotion_min_present=None, promotion_sale=None)
            return func

        for pr in PromotionSumPresent.objects.all():
            func = func_maker(pr, 'promotion_sum_present')
            text = 'sum_present_{}'.format(pr.id)
            actions[text] = (func, text, str(pr))

        for pr in PromotionThreeSales.objects.all():
            func = func_maker(pr, 'promotion_three_sales')
            text = 'three_sales_{}'.format(pr.id)
            actions[text] = (func, text, str(pr))

        for pr in PromotionMinPresent.objects.all():
            func = func_maker(pr, 'promotion_min_present')
            text = 'min_present_{}'.format(pr.id)
            actions[text] = (func, text, str(pr))

        for pr in PromotionSale.objects.all():
            func = func_maker(pr, 'promotion_sale')
            text = 'sale_{}'.format(pr.id)
            actions[text] = (func, text, str(pr))

        actions['delete_pr'] = (func_maker(), 'delete_pr', 'Убрать акции у товаров')

        return actions
