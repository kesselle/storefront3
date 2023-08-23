from typing import Any, List, Optional, Tuple
from django.contrib import admin
from django.db.models.query import QuerySet
from . import models
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
# Register your models here.


admin.site.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=['id', 'title']
    list_display=['title']

      

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<2345', 'High')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<2345':
            return queryset.filter(inventory__lt=2345)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status']
    list_editable = ['unit_price']
    list_per_page = 10
    list_filter = [InventoryFilter, 'last_update']  # Removed 'product' since it's not defined in your model

    @admin.display(ordering='inventory') 
    def inventory_status(self, product):
        if product.inventory > 2345:
            return 'High'
        return 'Ok'


@admin.register(models.Costumer)
class CostumertAdmin(admin.ModelAdmin):
    list_display= ['first_name', 'last_name', 'quantity_count' ,'membership']
    list_editable= ['membership']
    list_per_page=10
    list_select_related=['user']
    ordering=['user__first_name', 'user__last_name']
    search_fields=['first_name__istartswith', 'last_name__istartswith']
    

    @admin.display(ordering='quantity_count') 
    def quantity_count(self, costumer):
        url = reverse('admin:store3_costumer_change', args=[costumer.id]) + '?' + urlencode({'id': costumer.id})
        return format_html('<a href="{}">{}</a>', url, costumer.orderitem_set.count())
        
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            quantity_count=Count('orderitem')
        )
   




    

