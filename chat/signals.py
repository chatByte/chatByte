from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import Comment, Post, Profile, Inbox, PostInbox, Liked, Follower

host = "https://app-chatbyte.herokuapp.com/"
# host = "https://localhost:8000/"

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    # instance is a User object
    if created:
        try:
            instance.profile
        except:
            liked = Liked.objects.create()
            followers = Follower.objects.create()
            Profile.objects.create(id=host + "author/" + str(instance.id), user=instance,liked=liked, followers=followers)
        try:
            instance.inbox
        except:
            inbox = Inbox.objects.create(user=instance,)
            inbox.post_inbox = PostInbox.objects.create()
        Token.objects.create(user=instance)

        instance.profile.displayName = instance.username
        instance.profile.save()
        instance.inbox.post_inbox.author = instance.id
        instance.inbox.post_inbox.save()
        instance.inbox.save()

@receiver(post_save, sender=Post)
def create_post_signal(sender, instance, created, **kwargs):
    # instance is a Post object
    if created:
        # when create a Post object
        # instance.author is a Profile object
        # instance.author.id = host/author/<author id>

        # check if the instance id is a url that includes '/comments/'
        if "/posts/" not in str(instance.id):
            id_temp = instance.id
            # change to new id and save the instance as a new object
            instance.id = str(instance.author.id) + "/posts/" + str(instance.id)
            instance.comments_url = instance.id + '/comments/'
            # try:
            #     instance.liked
            # except:
            #     liked = Liked.objects.create()
            #     instance.liked = liked
            # try:
            #     instance.followers
            # except:
            #     followers = Follower.objects.create()
            #     instance.followers = followers
            instance.save()
            # # remove the old instance
            old_instance = Post.objects.get(pk=id_temp)
            old_instance.delete()

@receiver(post_save, sender=Comment)
def create_comment_signal(sender, instance, created, **kwargs):
    # instance is a Comment object
    if created:
        # when create a Comment object
        # instance.post_id = host/author/<author id>/posts/<posts id>
        # new_instance = instance

        # check if the instance id is a url that includes '/comments/'
        if "/comments/" not in str(instance.id):
            id_temp = instance.id
            # change to new id and save the instance as a new object
            instance.id = str(instance.parent_post.id) + "/comments/" + str(instance.id)
            instance.save()
            # remove the old instance
            old_instance = Comment.objects.get(pk=id_temp)
            old_instance.delete()
