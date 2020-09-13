from django.contrib import admin
from promotions.models import PromoCode, PromotionMinPresent, PromotionSale, PromotionSumPresent, PromotionThreeSales
from promotions.forms import PromotionSumPresentForm, PromotionMinPresentForm, PromotionSaleForm, PromotionThreeSalesForm
from products.models import Offer


@admin.register(PromotionSumPresent)
class PromotionSumPresentAdmin(admin.ModelAdmin):
    form = PromotionSumPresentForm

    def get_fields(self, request, obj=None):
        self.fields = ['total_price', 'price']

        if obj:
            self.fields.append('offers')

        return self.fields



@admin.register(PromotionThreeSales)
class PromotionThreeSalesAdmin(admin.ModelAdmin):
    form = PromotionThreeSalesForm

    def get_fields(self, request, obj=None):
        self.fields = [('price1', 'sale1'), ('price2', 'sale2'), ('price3', 'sale3')]

        if obj:
            self.fields.append('offers')

        return self.fields


@admin.register(PromotionMinPresent)
class PromotionMinPresentAdmin(admin.ModelAdmin):
    form = PromotionMinPresentForm

    def get_fields(self, request, obj=None):
        self.fields = ['nmb']

        if obj:
            self.fields.append('offers')

        return self.fields


@admin.register(PromotionSale)
class PromotionSaleAdmin(admin.ModelAdmin):
    form = PromotionSaleForm

    def get_fields(self, request, obj=None):
        self.fields = ['sale']

        if obj:
            self.fields.append('offers')

        return self.fields


admin.site.register(PromoCode)
