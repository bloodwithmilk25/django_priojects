from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from .models import Event
from datetime import datetime
# Create your views here.


def event_to_month(queryset):
    months = dict()
    for event in queryset():
        months[event.date.month] = event.month_str()
    return months


class UpcomingEventsView(ListView):
    model = Event
    template_name = 'events.html'

    def get_queryset(self):
        return Event.objects.filter(date__gte=datetime.today())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['months'] = event_to_month(self.get_queryset)
        return context


class PastEventsView(ListView):
    model = Event
    template_name = 'events.html'

    def get_queryset(self):
        return Event.objects.filter(date__lt=datetime.today())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['months'] = event_to_month(self.get_queryset)
        return context

# class PastEventsView(ArchiveIndexView):
#     model = Event
#     template_name = 'events.html'
#     date_field = 'date'
#     context_object_name = 'event_list'