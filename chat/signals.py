from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Comment, Post, Profile, Inbox, PostInbox

host = "https://chatbyte.herokuapp.com"

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    # instance is a User object
    if created:
        try:
            instance.profile
        except:
            Profile.objects.create(user=instance,)
        try:
            instance.inbox
        except:
            inbox = Inbox.objects.create(user=instance,)
            inbox.post_inbox = PostInbox.objects.create()
        Token.objects.create(user=instance)
    instance.profile.displayName = instance.username
    instance.profile.id = host + "/author/" + str(instance.id)
    instance.profile.save()
    instance.inbox.post_inbox.author = instance.id
    instance.inbox.post_inbox.save()
    instance.inbox.save()

@receiver(post_save, sender=Post)
def update_post_signal(sender, instance, created, **kwargs):
    # instance is a Post object
    if created:
        # when create a Post object
        # instance.author is a Profile object
        # instance.author.id = host/author/<author id>
        instance.id = instance.author.id + "/posts/" + str(instance.id)
    instance.save()

@receiver(post_save, sender=Comment)
def update_post_signal(sender, instance, created, **kwargs):
    # instance is a Comment object
    if created:
        # when create a Post object
        # instance.post_id = host/author/<author id>/posts/<posts id>
        instance.id = instance.post_id + "/comments/" + str(instance.id)
    instance.save()

@receiver(post_save, sender=Comment)
def update_post_signal(sender, instance, created, **kwargs):
    # instance is a Comment object
    if created:
        # when create a Post object
        # instance.post_id = host/author/<author id>/posts/<posts id>
        instance.id = instance.post_id + "/comments/" + str(instance.id)
    instance.save()