from django import forms
from .models import Visitor

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        exclude = ('verified','qrcode') # first_name, last_name, email,
        # phone_number, position, comptany, country

    # checks for unick fields
    def clean(self):
        cleaned_data = super(VisitorForm, self).clean()
        # additional cleaning here
        return cleaned_data
