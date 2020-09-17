from django.contrib import admin
from promotions.models import PromoCode, PromotionMinPresent, PromotionSale, PromotionSumPresent, PromotionThreeSales
from products.models import Offer


admin.site.register(PromoCode)
admin.site.register(PromotionMinPresent)
admin.site.register(PromotionSale)
admin.site.register(PromotionSumPresent)


@admin.register(PromotionThreeSales)
class PromotionThreeSalesAdmin(admin.ModelAdmin):
    fields = ('text', ('price1', 'sale1'), ('price2', 'sale2'), ('price3', 'sale3'))
