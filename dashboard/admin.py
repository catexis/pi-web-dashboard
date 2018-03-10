from django.contrib import admin

# Register your models here.
from . import models

@admin.register(models.PricePosition)
class PricePositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

@admin.register(models.PricePrice)
class PricePriceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'price', 'in_stock')