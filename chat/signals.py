from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Profile

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:     
        try:
            instance.profile
        except:
            Profile.objects.create(user=instance,)
            Token.objects.create(user=instance)
    instance.profile.displayName = instance.username
    instance.profile.id = instance.id
    instance.profile.save()