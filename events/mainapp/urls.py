from django.urls import re_path
from . import views

app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', views.UpcomingEventsView.as_view(), name='upcoming'),
    re_path(r'archive/$', views.PastEventsView.as_view(), name='past'),
]
