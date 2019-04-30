from django.urls import re_path
from . import views

app_name = "portf"

urlpatterns = [
    re_path(r'about/$', views.AboutView.as_view(), name='about'),
    re_path(r'contact/$', views.ContactView.as_view(), name='contact'),
    re_path(r"^$", views.HomePageView.as_view(), name="home"),
]