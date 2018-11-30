from .models import Order
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=20,required=True)
    email = forms.EmailField(max_length=35,required=True)
    class Meta:
        fields = ("username","first_name", "last_name", "email","password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args,**kwargs)
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            raise forms.ValidationError("That combination of username and email are already in use")

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name',
                   'last_name',
                   'phone',
                   'shipping_type',
                   'shipping_adress',
                   'comments')
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'
