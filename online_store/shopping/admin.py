from django.contrib import admin
from shopping.models import *
# Register your models here.

def make_payed(modeladmin, request, queryset):
    queryset.update(status='completed')
make_payed.short_description = 'Mark as completed'

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_payed]

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order,OrderAdmin)
