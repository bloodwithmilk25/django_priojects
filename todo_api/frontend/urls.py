from django.urls import re_path
from frontend import views
app_name = "frontend"

urlpatterns = [
    re_path(r'^$', views.MainPage.as_view(), name='mainpage'),
]