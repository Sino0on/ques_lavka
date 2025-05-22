from django.contrib import admin
from .models import *


admin.site.register(Faq)
admin.site.register(SiteSetting)
from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'product_list', 'promo_code')
    readonly_fields = ('product_list',)
    exclude = ('products',)  # скрываем оригинальное поле products
    search_fields = ('user__email', 'promo_code')
    list_filter = ('created_at',)

    def product_list(self, obj):
        return "\n".join([f"• {p.name}" for p in obj.products.all()])

    product_list.short_description = "Товары в заказе"



admin.site.register(FreedomPayConfig)
