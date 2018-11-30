from django.contrib import admin
from .models import Speaker, Confrence, Report, Visitor
# Register your models here.

class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','company',)
    #list_filter = ('created',)
    search_fields = ('last_name',)

class ConfrenceAdmin(admin.ModelAdmin):
    list_display = ('name','date')
    list_filter = ('date',)
    search_fields = ('name',)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title','speaker','date','order')
    list_filter = ('date',)
    search_fields = ('title','speaker',)

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','company','verified',)
    list_filter = ('verified',)
    search_fields = ('first_name','last_name','email',)


admin.site.register(Speaker,SpeakerAdmin)
admin.site.register(Confrence,ConfrenceAdmin)
admin.site.register(Report,ReportAdmin)
admin.site.register(Visitor,VisitorAdmin)
