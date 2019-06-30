from django.contrib import admin
from .models import Movie, Director, Tag
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.

admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Tag)
#TokenAdmin.raw_id_fields = ('user',)
