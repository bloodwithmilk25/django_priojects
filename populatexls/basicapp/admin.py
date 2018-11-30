from django.contrib import admin
from .models import Visitor, Test, Test2
# Register your models here.


class TestAdmin(admin.ModelAdmin):
    list_display = ('one', 'two', 'three', 'four', 'five')


admin.site.register(Visitor)
admin.site.register(Test, TestAdmin)
admin.site.register(Test2, TestAdmin)

