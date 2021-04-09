from django import forms
from django.conf import settings
from django.core.validators import FileExtensionValidator

from django.contrib.auth.models import User
# from .models import Profile, NewPost
# from .models import Profile
from .widgets import AdminPagedownWidget, PagedownWidget

IMAGE_UPLOAD_EXTENSIONS = getattr(
    settings,
    'PAGEDOWN_IMAGE_UPLOAD_EXTENSIONS', [
        'jpg',
        'jpeg',
        'png',
        'webp'
    ])

# creating a form
# Profile form, that can passing profile info
class ProfileForm(forms.Form):
    display_name = forms.CharField(max_length=200)
    # last_name = forms.CharField(max_length=200)
    URL = forms.URLField(max_length=200)
    GITHUB = forms.URLField(max_length=200)
    email = forms.CharField(max_length=200)


# class PagedownField(forms.CharField):
#     widget = PagedownWidget


# class AdminPagedownField(forms.CharField):
#     widget = AdminPagedownWidget


# class ImageUploadForm(forms.Form):
#     image = forms.ImageField(
#         required=True,
#         validators=[FileExtensionValidator(
#             allowed_extensions=IMAGE_UPLOAD_EXTENSIONS)])
