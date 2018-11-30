from django.contrib import admin
from .models import Todo
# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    list_display = ('name', 'completed', 'created_date', 'id')


admin.site.register(Todo, TodoAdmin)