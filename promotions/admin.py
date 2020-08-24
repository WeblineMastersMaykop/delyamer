from django.contrib import admin
from promotions.models import Promotion, PromoCode
# from products.models import Offer


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('promotion_type', 'main_text', 'url')
    filter_horizontal = ('products',)

    def get_fields(self, request, obj=None):
        self.fields = ['promotion_type']

        if obj:
            if obj.promotion_type == 'type1':
                add_fields = ('type1_sum', 'type1_price')
                self.fields.extend(add_fields)

            if obj.promotion_type == 'type2':
                add_fields = (('type2_price1', 'type2_sale1'),
                              ('type2_price2', 'type2_sale2'),
                              ('type2_price3', 'type2_sale3'))
                self.fields.extend(add_fields)

            if obj.promotion_type == 'type3':
                self.fields.append('type3_nmb')

            if obj.promotion_type == 'type4':
                self.fields.append('type4_sale')

        add_fields = ('main_text', 'sub_text', 'url', 'image', 'products')
        self.fields.extend(add_fields)
        return self.fields

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == 'products':
    #         kwargs['queryset'] = Offer.objects.filter(is_active=r)
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)

    class Media:
        js = ('/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              '/static/grappelli/tinymce_setup/tinymce_setup.js')


admin.site.register(PromoCode)
