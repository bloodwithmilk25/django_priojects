from django.contrib import admin
from .models import Picture, Contact
# Register your models here.


class PicturesAdmin(admin.ModelAdmin):
    list_display = ('name', 'page')
    list_filter = ('name', 'page')


admin.site.register(Picture, PicturesAdmin)
admin.site.register(Contact)
