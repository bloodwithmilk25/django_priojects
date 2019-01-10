from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from .forms import VisitorForm
from .models import Visitor, Speaker
# Create your views here.

# commit

class HomePageView(TemplateView):
    template_name = 'home.html'


class ContactPageView(TemplateView):
    template_name = 'contact.html'


class SpeakerListView(ListView):
    model = Speaker


class VisitorRegistration(CreateView):
    form_class = VisitorForm
    model = Visitor
    success_url = reverse_lazy("event:home")

    def form_valid(self, form):
        if self.request.recaptcha_is_valid:
            visitor = form.save()
            current_site = get_current_site(self.request)
            mail_subject = 'Confirm you really want to visit us, check EMAIL.'
            message = render_to_string('visitor_activate_email.html', {
                'visitor': visitor.first_name +' '+ visitor.last_name,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(visitor.pk)).decode(),
                'token':account_activation_token.make_token(visitor),
            })
            email = EmailMessage(mail_subject, message, to=[visitor.email])
            email.send()
            return render(self.request, 'thank_you.html')
        return render(self.request, 'visitor_form.html', self.get_context_data())


def activate(request, uidb64, token):
    try:
        vid = force_text(urlsafe_base64_decode(uidb64))
        visitor = Visitor.objects.get(pk=vid)
    except(TypeError, ValueError, OverflowError, Visitor.DoesNotExist):
        visitor = None
    if visitor is not None and account_activation_token.check_token(visitor, token):

        context = {'name': visitor.first_name + " " + visitor.last_name,
                   'email': visitor.email,
                   'phone': visitor.phone_number,
                   'position': visitor.position,
                   'company': visitor.company}

        if not visitor.verified: # if it's a completely new user
            visitor.activate()
            visitor.save()
            visitor.generate_qr_code(request)
            context['qrcode'] = visitor.qrcode
            # send ticket url to email
            message = '''Here is your ticker, you will need it
                         to enter the conference \n''' + request.build_absolute_uri()
            email = EmailMessage('noreply', message, to=[visitor.email])
            email.send()
            # and also render ticket to user
            return render(request, 'ticket.html', context=context)
        else: #if user is already verified and has a qrocode:
            context['qrcode'] = visitor.qrcode
            return render(request, 'ticket.html', context=context)
    else:
        return render(request, 'invalid_activation_link.html')
