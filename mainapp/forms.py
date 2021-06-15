import django.forms as forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhonePrefixSelect, PhoneNumberInternationalFallbackWidget
from .models import Profile


class RegisterForm(forms.ModelForm):

    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'input',
                                                                          'placeholder': 'example@example.com'}))
    phone_number = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget(attrs={'placeholder': '+79999999999', "class": 'input'}
                                                      , region="RU")
    )

    class Meta:

        model = Profile
        fields = ['phone_number', 'email']
