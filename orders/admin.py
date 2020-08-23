from django.contrib import admin
from orders.models import DeliveryMethod, Order, OrderStatus, OrderItem


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'price')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    classes = ('grp-collapse grp-closed',)
    autocomplete_fields = ('offer',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'delivery', 'status', 'created', 'updated')
    inlines = (OrderItemInline,)


admin.site.register(OrderStatus)
