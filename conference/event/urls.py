from django.urls import re_path
from . import views
from .decorators import check_recaptcha

app_name = 'event'

urlpatterns = [
    re_path(r'^$',views.HomePageView.as_view(),name='home'),
    re_path(r'contact/$',views.ContactPageView.as_view(),name='contact'),
    re_path(r'registration/$',check_recaptcha(views.VisitorRegistration.as_view()),name='register'),
    re_path(r'speakers/$',views.SpeakerListView.as_view(),name='speakers'),
    re_path(r"activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$", views.activate, name='activate'),
]
