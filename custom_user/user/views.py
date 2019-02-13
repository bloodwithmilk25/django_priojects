from django.views import View
from django.http import HttpResponse
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

from .models import User
from .tokens import account_activation_token
from .forms import UserCreationForm,  UserUpdateForm


class SignUp(View):
    template_name = "user/registration/signup.html"
    form = UserCreationForm

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('confirm')

        context = {
            'form': form
        }
        
        return render(request, self.template_name, context)


def verify(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        login(request, user)
        return redirect('profile')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def update_user(request):
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, 'user/update_user.html', {'form': form})


@login_required
def resent_email(request):
    if request.method == 'GET':
        user = request.user
        print(user)
        mail_subject = 'Activate your account.'
        message = render_to_string('account_activation_email.html', {
            'user': user,
            'domain': 'http://localhost:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(mail_subject, message)
        return redirect('profile')
