from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        strip=True,
    )
    email = forms.EmailField()
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Username already exists.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Email already exists.')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', 'Passwords do not match.')

        if password:
            try:
                validate_password(
                    password,
                    user=User(
                        username=cleaned_data.get('username', ''),
                        email=cleaned_data.get('email', ''),
                    ),
                )
            except ValidationError as error:
                self.add_error('password', error)

        return cleaned_data
