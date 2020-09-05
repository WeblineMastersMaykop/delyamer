from django import forms
from django.db.models import Q
# from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple
from products.models import Offer


# class PromotionModelForm(forms.ModelForm):
#     def clean_offers(self):
#         super(PromotionModelForm, self).clean()
#         offers = self.cleaned_data.get('offers')
#         promotion_type = self.cleaned_data.get('promotion_type')

#         error_offers = []
#         for offer in offers:
#             if Promotion.objects.filter(promotion_type=promotion_type).filter(offers=offer):
#                 error_offers.append(offer)

#         if error_offers:
#             offer_list = '; '.join('<' + str(error_offer) + '>' for error_offer in error_offers)
#             raise ValidationError('Следующие варианты товаров уже учавствует в подобной акции: {}'.format(offer_list))

#         return offers


class PromotionSumPresentForm(forms.ModelForm):

    offers = forms.ModelMultipleChoiceField(
        queryset=Offer.objects.filter(is_active=True),
        label='Вариаты товаров',
        required=False,
        widget=FilteredSelectMultiple('Варианты товара', False)
    )

    def __init__(self, *args, **kwargs):
        super(PromotionSumPresentForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['offers'].initial = self.instance.offers.all()
            self.fields['offers'].queryset = self.fields['offers'].queryset.filter(Q(promotion_sum_present=None) | Q(promotion_sum_present=self.instance))
    def save(self, *args, **kwargs):
        instance = super(PromotionSumPresentForm, self).save(commit=False)
        old_offers = self.instance.offers.all()
        new_offers = self.cleaned_data['offers']

        for offer in old_offers:
            offer.promotion_sum_present = None

        for offer in new_offers:
            offer.promotion_sum_present = instance

        Offer.objects.bulk_update(old_offers, ['promotion_sum_present'])
        Offer.objects.bulk_update(new_offers, ['promotion_sum_present'])

        return instance


class PromotionThreeSalesForm(forms.ModelForm):

    offers = forms.ModelMultipleChoiceField(
        queryset=Offer.objects.filter(is_active=True),
        label='Вариаты товаров',
        required=False,
        widget=FilteredSelectMultiple('Варианты товара', False)
    )

    def __init__(self, *args, **kwargs):
        super(PromotionThreeSalesForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['offers'].initial = self.instance.offers.all()
            self.fields['offers'].queryset = self.fields['offers'].queryset.filter(Q(promotion_three_sales=None) | Q(promotion_three_sales=self.instance))

    def save(self, *args, **kwargs):
        instance = super(PromotionThreeSalesForm, self).save(commit=False)
        old_offers = self.instance.offers.all()
        new_offers = self.cleaned_data['offers']

        for offer in old_offers:
            offer.promotion_three_sales = None

        for offer in new_offers:
            offer.promotion_three_sales = instance

        Offer.objects.bulk_update(old_offers, ['promotion_three_sales'])
        Offer.objects.bulk_update(new_offers, ['promotion_three_sales'])

        return instance


class PromotionMinPresentForm(forms.ModelForm):

    offers = forms.ModelMultipleChoiceField(
        queryset=Offer.objects.filter(is_active=True),
        label='Вариаты товаров',
        required=False,
        widget=FilteredSelectMultiple('Варианты товара', False)
    )

    def __init__(self, *args, **kwargs):
        super(PromotionMinPresentForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['offers'].initial = self.instance.offers.all()
            self.fields['offers'].queryset = self.fields['offers'].queryset.filter(Q(promotion_min_present=None) | Q(promotion_min_present=self.instance))

    def save(self, *args, **kwargs):
        instance = super(PromotionMinPresentForm, self).save(commit=False)
        old_offers = self.instance.offers.all()
        new_offers = self.cleaned_data['offers']

        for offer in old_offers:
            offer.promotion_min_present = None

        for offer in new_offers:
            offer.promotion_min_present = instance

        Offer.objects.bulk_update(old_offers, ['promotion_min_present'])
        Offer.objects.bulk_update(new_offers, ['promotion_min_present'])

        return instance


class PromotionSaleForm(forms.ModelForm):

    offers = forms.ModelMultipleChoiceField(
        queryset=Offer.objects.filter(is_active=True),
        label='Вариаты товаров',
        required=False,
        widget=FilteredSelectMultiple('Варианты товара', False)
    )

    def __init__(self, *args, **kwargs):
        super(PromotionSaleForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['offers'].initial = self.instance.offers.all()
            self.fields['offers'].queryset = self.fields['offers'].queryset.filter(Q(promotion_sale=None) | Q(promotion_sale=self.instance))

    def save(self, *args, **kwargs):
        instance = super(PromotionSaleForm, self).save(commit=False)
        old_offers = self.instance.offers.all()
        new_offers = self.cleaned_data['offers']

        for offer in old_offers:
            offer.promotion_sale = None

        for offer in new_offers:
            offer.promotion_sale = instance

        if old_offers:
            Offer.objects.bulk_update(old_offers, ['promotion_sale'])

        if new_offers:
            Offer.objects.bulk_update(new_offers, ['promotion_sale'])

        return instance
