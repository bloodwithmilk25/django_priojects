from django.urls import re_path
from . import views

app_name = 'events'

urlpatterns = [
    re_path(r'^$', views.UpcomingEventsView.as_view(), name='upcoming'),
    re_path(r'past/$', views.PastEventsView.as_view(), name='past'),
    re_path(r'archive/$', views.ArchiveEventsView.as_view(), name='archive'),
    re_path(r'event/(?P<slug>[-\w]+)/$', views.EventDetailView.as_view(), name='event_detail'),
    re_path(r'location/(?P<pk>\d+)/$', views.LocationDetailView.as_view(), name='location_detail'),
    re_path(r"search/", views.search, name="search"),
]
