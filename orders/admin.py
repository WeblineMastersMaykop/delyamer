from django.contrib import admin
from orders.models import Order, OrderItem, Review, DeliveryMethod


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    classes = ('grp-collapse grp-closed',)
    autocomplete_fields = ('offer',)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    classes = ('grp-collapse grp-closed',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'delivery', 'delivery_price', 'status', 'pay_type', 'total_price', 'total_price_with_sale', 'sync_1c', 'track_number', 'created', 'updated')
    list_filter = ('status', 'delivery', 'pay_type')
    list_editable = ('sync_1c',)
    search_fields = ('full_name', 'user__full_name', 'user__username')
    inlines = (OrderItemInline,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'rating', 'created', 'updated')
    search_fields = ('order_item__order__offer__product__name', 'order_item__order__user__username', 'order_item__order__user__full_name', 'rating')
