from django.views.generic import TemplateView
from django.http import HttpRequest
from api.models import Todo
# Create your views here.


class MainPage(TemplateView):
    template_name = 'foo.html'