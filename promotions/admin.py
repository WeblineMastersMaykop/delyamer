from django.contrib import admin
from promotions.models import PromoCode, PromotionMinPresent, PromotionSale, PromotionSumPresent, PromotionThreeSales
from promotions.forms import PromotionSumPresentForm, PromotionMinPresentForm, PromotionSaleForm, PromotionThreeSalesForm
from products.models import Offer


# class OfferInline(admin.TabularInline):
#     model = Offer
#     extra = 0
#     raw_id_fields = ('promotion_sum_present',)


@admin.register(PromotionSumPresent)
class PromotionSumPresentAdmin(admin.ModelAdmin):
    # fields = ('offer_sum', 'price', 'main_text', 'sub_text', 'url', 'image', 'offers')
    form = PromotionSumPresentForm
    # raw_id_fields = ('offers', )
    # list_display = ('offer_sum', 'price')
    # filter_horizontal = ('offers',)

    def get_fields(self, request, obj=None):
        self.fields = ['offer_sum', 'price', 'main_text', 'sub_text', 'url', 'image']

        if obj:
            self.fields.append('offers')

        return self.fields

    # def get_fields(self, request, obj=None):
    #     self.fields = ['promotion_type']

    #     if obj:
    #         if obj.promotion_type == 'type1':
    #             add_fields = ('type1_sum', 'type1_price')
    #             self.fields.extend(add_fields)

    #         if obj.promotion_type == 'type2':
    #             add_fields = (('type2_price1', 'type2_sale1'),
    #                           ('type2_price2', 'type2_sale2'),
    #                           ('type2_price3', 'type2_sale3'))
    #             self.fields.extend(add_fields)

    #         if obj.promotion_type == 'type3':
    #             self.fields.append('type3_nmb')

    #         if obj.promotion_type == 'type4':
    #             self.fields.append('type4_sale')

    #     add_fields = ('main_text', 'sub_text', 'url', 'image', 'offers')
    #     self.fields.extend(add_fields)
    #     return self.fields

    # class Media:
    #     js = ('/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
    #           '/static/grappelli/tinymce_setup/tinymce_setup.js')


# @admin.register(PromotionEdit)
# class PromotionEditAdmin(admin.ModelAdmin):
#     list_display = ('product', 'offer', 'color', 'cup', 'size')
#     inlines = (OfferInline,)


@admin.register(PromotionThreeSales)
class PromotionThreeSalesAdmin(admin.ModelAdmin):
    form = PromotionThreeSalesForm

    def get_fields(self, request, obj=None):
        self.fields = [('price1', 'sale1'), ('price2', 'sale2'), ('price3', 'sale3'), 'main_text', 'sub_text', 'url', 'image']

        if obj:
            self.fields.append('offers')

        return self.fields


@admin.register(PromotionMinPresent)
class PromotionMinPresentAdmin(admin.ModelAdmin):
    form = PromotionMinPresentForm

    def get_fields(self, request, obj=None):
        self.fields = ['nmb', 'main_text', 'sub_text', 'url', 'image']

        if obj:
            self.fields.append('offers')

        return self.fields


@admin.register(PromotionSale)
class PromotionSaleAdmin(admin.ModelAdmin):
    form = PromotionSaleForm

    def get_fields(self, request, obj=None):
        self.fields = ['sale', 'main_text', 'sub_text', 'url', 'image']

        if obj:
            self.fields.append('offers')

        return self.fields


admin.site.register(PromoCode)
