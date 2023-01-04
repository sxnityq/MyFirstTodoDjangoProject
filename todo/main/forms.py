from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser
from .utils import custom_send_mail

from django import forms
from django.core.exceptions import ValidationError


class CustomAuthForm(AuthenticationForm):
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request,
                email=email,
                password=password
            )
            if not self.user_cache.email_verify:
                custom_send_mail(self.request, self.user_cache)
                raise ValidationError('email not verify? Check your email',
                                      code='invalid_login')
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=32,
                               widget=(forms.TextInput(attrs={'class': 'form-entity'})))
    email = forms.EmailField(max_length=64,
                             widget=(forms.EmailInput(attrs={'class': 'form-entity'})))
    password1 = forms.CharField(max_length=32,
                                widget=(forms.PasswordInput(attrs={'class': 'form-entity'})))
    password2 = forms.CharField(max_length=32,
                                widget=(forms.PasswordInput(attrs={'class': 'form-entity'})))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class UpdateUserProfile(forms.ModelForm):
    username = forms.CharField(max_length=32,
                               widget=(forms.TextInput(attrs={'class': 'form-entity'})))
    profile_image = forms.ImageField(max_length=64,
                                     widget=(forms.FileInput(attrs={'class': 'form-entity'})))

    class Meta:
        model = CustomUser
        fields = ('username', 'profile_image')
