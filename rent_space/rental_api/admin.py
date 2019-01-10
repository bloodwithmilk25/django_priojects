from django.contrib import admin
from .models import Cell
# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "row", "column", "taken", "occupied_by")


admin.site.register(Cell, TodoAdmin)