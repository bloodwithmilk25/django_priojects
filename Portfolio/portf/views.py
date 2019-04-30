from django.views.generic import TemplateView,ListView,CreateView
from .models import Picture, Contact
from .forms import ContactForm


class HomePageView(TemplateView):
    template_name = 'home.html'
    model = Picture

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for picture in self.model.objects.filter(page='homepage'):
            context[picture.name] = picture.path.url
        return context


class AboutView(TemplateView):
    template_name = 'about.html'
    model = Picture

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_photo = self.model.objects.get(name='me')
        context['me'] = my_photo.path.url
        return context


class ContactView(CreateView):
    redirect_field_name = 'home.html'
    form_class = ContactForm
    model = Contact
