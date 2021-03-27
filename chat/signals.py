from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Profile, Inbox, PostInbox

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
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
    instance.profile.id = instance.id
    instance.profile.save()
    instance.inbox.post_inbox.author = instance.id
    instance.inbox.post_inbox.save()
    instance.inbox.save()
