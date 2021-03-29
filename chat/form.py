from django import forms
from django.contrib.auth.models import User
from .models import Profile

# creating a form
# Profile form, that can passing profile info
class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    URL = forms.CharField(max_length=200)
    GITHUB = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)


