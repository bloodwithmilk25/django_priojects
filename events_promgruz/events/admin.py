from django.contrib import admin
from .models import Category, Tag, Location, Event, Image
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields


class ImageInline(admin.TabularInline):
    model = Image
    extra = 4


class LocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField:
            {'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
    }
    inlines = [ImageInline]
    list_display = ('name', 'country', 'city')
    list_filter = ('name', 'country', 'city')
    search_fields = ('name', 'country')


# admin actions for "Event" model
def publish(modeladmin, request, queryset):
    queryset.update(published=True)
publish.short_description = "Опубликовать выбранные"

def unpublish(modeladmin, request, queryset):
    queryset.update(published=False)
unpublish.short_description = "Выбранные в черновик"


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'parent_event', 'date_start', 'published')
    list_filter = ('category', 'tag', 'parent_event', 'date_start', 'published')
    search_fields = ('name', 'date_start')
    actions = [publish, unpublish]

    def get_queryset(self, request):
        return Event.objects.get_queryset(all=True)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = 'events',
    search_fields = ('name', 'slug')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'events')
    list_filter = 'events',
    search_fields = ('name', 'slug', 'events')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order')
    list_filter = ('location', 'event')
    search_fields = ('location.name', 'event.name')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Image, ImageAdmin)
