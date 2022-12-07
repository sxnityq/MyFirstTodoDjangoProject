from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser
from .utils import *

from django import forms

class RegisterUserForm(UserCreationForm):
    
    username = forms.CharField(max_length=32, widget=(forms.TextInput(attrs={'class' : 'form-entity'})))
    email = forms.EmailField(max_length=64, widget=(forms.EmailInput(attrs={'class' : 'form-entity'})))
    password1 = forms.CharField(max_length=32, widget=(forms.PasswordInput(attrs={'class' : 'form-entity'})))
    password2 = forms.CharField(max_length=32, widget=(forms.PasswordInput(attrs={'class' : 'form-entity'})))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class UpdateUserProfile(forms.ModelForm):
    
    username= forms.CharField(max_length=32, widget=(forms.TextInput(attrs={'class' : 'form-entity'})))
    profile_image = forms.ImageField(max_length=64, widget=(forms.FileInput(attrs={'class' : 'form-entity'})))

    class Meta:
        model = CustomUser
        fields = ('username', 'profile_image')