from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Bus


class StudentRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, label='Full Name')
    email = forms.EmailField(label='Gmail Address')
    place = forms.CharField(max_length=150, label='Place', required=False)
    bus = forms.ModelChoiceField(queryset=Bus.objects.filter(is_active=True), label='Bus Number')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.lower().endswith('@gmail.com'):
            raise forms.ValidationError('Please use a Gmail address to register.')
        return email.lower()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['name', 'route', 'capacity', 'driver_name', 'driver_phone']
        labels = {
            'name': 'Bus Number',
            'route': 'Route',
            'capacity': 'Capacity',
            'driver_name': 'Driver Name',
            'driver_phone': 'Driver Phone',
        }


class BoardingForm(forms.Form):
    boarding_place = forms.CharField(max_length=200, label='Boarding Place')


class ExitForm(forms.Form):
    exit_place = forms.CharField(max_length=200, label='Exit Place')
