from .forms import UserAuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import User
from django.core.mail import EmailMessage
from django.views import View


class SignUp(View):
    template_name = "user/registration/signup.html"
    form = UserCreationForm

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        done = False
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password1'])
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            done = True

        context = {
            'form': form,
            'done': done
        }

        return render(request, self.template_name, context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


# class Login(View):
#     template_name = "login.html"
#     form = UserAuthenticationForm
#
#     def get(self, request):
#         form = self.form()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         fail = False
#         form = self.form(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(email=cd['email'], password=cd['password'])
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 fail = True
#
#         context = {
#             'form': form,
#         }
#
#         return render(request, self.template_name, context)
