from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Profile

from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ('user',)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)