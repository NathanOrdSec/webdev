from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Users

class RegisterForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['username','handle','password1','password2'] 