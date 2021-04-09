from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Profile, FriendRequest, Follower, Inbox, PostInbox, Like, Liked, Node

from rest_framework.authtoken.admin import TokenAdmin
# from pagedown.widgets import AdminPagedownWidget

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin

class UserAdmin(OriginalUserAdmin):
    actions = ['activate_user','deactivate_user']

    def activate_user(self, request, queryset):
        queryset.update(is_active=True)

    def deactivate_user(self, request, queryset):
        queryset.update(is_active=False)

    activate_user.short_description = "Activate selected users"
    deactivate_user.short_description = "Deactivate selected users"

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


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