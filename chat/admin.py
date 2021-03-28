from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Profile, FriendRequest, Followers, Inbox, PostInbox, Like, Liked

from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ('user',)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Followers)
admin.site.register(PostInbox)
admin.site.register(Inbox)
admin.site.register(Like)
admin.site.register(Liked)