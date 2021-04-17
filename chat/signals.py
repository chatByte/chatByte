from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import *


# multi host can be easily change here
host = "https://chatbyte.herokuapp.com/"
# host = "http://127.0.0.1:8000/"
# host = "https://app-chatbyte.herokuapp.com/"
# host = "https://chatbyte.herokuapp.com/"
# host = "https://localhost:8000/"



"""
design for handling update_profile_signal , to update db 
"""
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    # instance is a User object
    if created:
        try:
            Node.objects.get(username=instance.username)
        except:
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
            instance.profile.url = instance.id
            instance.profile.host = host
            instance.profile.save()
            instance.inbox.post_inbox.author = instance.id
            instance.inbox.post_inbox.save()
            instance.inbox.save()


"""
design for handling create_post_signal , to update db 
"""
@receiver(post_save, sender=Post)
def create_post_signal(sender, instance, created, **kwargs):
    # instance is a Post object
    if created:
        # when create a Post object

        # check if the instance id is a url that includes '/comments/'
        if "/posts/" not in str(instance.id):
            id_temp = instance.id
            # change to new id and save the instance as a new object
            instance.id = str(instance.author.id) + "/posts/" + str(instance.id)
            instance.comments_url = instance.id + '/comments/'

            instance.save()
            # # remove the old instance
            old_instance = Post.objects.get(pk=id_temp)
            old_instance.delete()


"""
design for handling create_comment_signal , to update db 
"""
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


"""
design for handling create_node_signal , to update db 
"""
@receiver(post_save, sender=Node)
def create_node_signal(sender, instance, created, **kwargs):
    # instance is a Node object
    if created:
        # when create a Node object
        # create a user with the corresponding credential

        # check if the instance id is a url that includes '/comments/'
        user = User.objects.create_user(instance.username, password=instance.password)
        user.first_name = instance.password
        user.last_name = instance.origin
        user.is_superuser = False
        user.is_staff = False
        user.save()
