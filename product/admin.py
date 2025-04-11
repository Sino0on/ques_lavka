from django.contrib import admin
from .models import *

# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ImageProduct)

class ImagesInline(admin.StackedInline):
    model = ImageProduct
    extra = 0
    # filter_horizontal = ('floorschemas',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImagesInline,
    ]