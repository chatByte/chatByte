from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Profile, FriendRequest, Follower, Inbox, PostInbox, Like, Liked, Node

from rest_framework.authtoken.admin import TokenAdmin
from pagedown.widgets import AdminPagedownWidget

TokenAdmin.raw_id_fields = ('user',)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Follower)
admin.site.register(PostInbox)
admin.site.register(Inbox)
admin.site.register(Like)
admin.site.register(Liked)
admin.site.register(Node)