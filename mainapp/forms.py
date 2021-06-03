import django.forms as forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import Profile


class RegisterForm(forms.ModelForm):

    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(initial='RU')
    )

    class Meta:

        model = Profile
        fields = ['email', 'phone_number', 'messenger']