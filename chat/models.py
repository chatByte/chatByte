from django.db import models
import uuid
import django
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
# class Actor(models.Model):
#     # for authorization only
#     ID = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
#     USERNAME = models.CharField(max_length=50, unique=True)


class Profile(models.Model):
    type = models.CharField(max_length=200, default="author")
    id = models.CharField(max_length=200, primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    host = models.URLField(max_length=200, null=True)
    displayName = models.CharField(max_length=200, null=True)
    url = models.URLField(max_length=200, null=True)
    github = models.URLField(max_length=200, null=True)

    # a group of author, that i accepted to be my friend
    friends = models.ManyToManyField("Profile", related_name='%(class)s_friends', blank=True)
    # a group of author, that  followed me
    followers = models.OneToOneField("Follower", on_delete=models.CASCADE, null=True, blank=True)
    # a group of author, that i am currently following
    followings = models.ManyToManyField("Profile", related_name='%(class)s_followings', blank=True)
    timeline = models.ManyToManyField("Post", blank=True)
    # the friend request i received
    friend_requests = models.ManyToManyField("FriendRequest", related_name='%(class)s_friend_requests', blank=True)
    # the friend request i snet
    friend_requests_sent = models.ManyToManyField("FriendRequest", related_name='%(class)s_friend_requests_sent', blank=True)
    # the iteams, that i currenly liked
    liked = models.OneToOneField('Liked', on_delete=models.CASCADE, null=True, blank=True)

    def __unicode__(self): # for Python 2
        return self.user.username

    # class Meta:
    #     managed = False

class Comment(models.Model):
    type = models.CharField(max_length=200, default="comment")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)

    author = models.ForeignKey('Profile', on_delete=models.CASCADE,)

    comment = models.TextField()
    contentType = models.CharField(max_length=200)
    published = models.DateTimeField(default=django.utils.timezone.now)
    likes = models.ManyToManyField('Like', blank=True)
    # # the father of Comeent is POST
    parent_post = models.ForeignKey("Post", on_delete= models.CASCADE)



class Post(models.Model):
    type = models.CharField(max_length=200, default="post")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    title = models.TextField()
    # where did you get this post from?
    source = models.URLField(max_length=200)
    # where is it actually from
    origin = models.URLField(max_length=200)
    description = models.TextField()
    contentType = models.CharField(max_length=200)
    content = models.TextField()
    # the author has an ID where by authors can be disambiguated
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    categories = ArrayField(
        models.CharField(max_length=200, blank=True),
        size=200,
    )
    count = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    comments_url = models.CharField(max_length=200)
    comments = models.ManyToManyField('Comment', blank=True)
    # published date
    published = models.DateTimeField(default=django.utils.timezone.now)
    visibility = models.CharField(max_length=50)
    unlisted = models.CharField(max_length=50, default='false', editable=False)
    likes = models.ManyToManyField('Like', blank=True)

class PostInbox(models.Model):
    type = models.CharField(max_length=200, default="inbox", blank=True)
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    author = models.CharField(max_length=200, blank=True, null=True)
    items = models.ManyToManyField('Post', blank=True)

class Inbox(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    post_inbox = models.OneToOneField('PostInbox', on_delete=models.CASCADE, null=True, blank=True)
    like_inbox = models.ManyToManyField('Like', blank=True)
    friend_requests = models.ManyToManyField('FriendRequest', blank=True)

class Follower(models.Model):
    # get a list of authors who are their followers
    type = models.CharField(max_length=200, default="followers")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    # Here items are Authors , which is Profiles
    items = models.ManyToManyField('Profile', related_name='%(class)s_followers_items', blank=True)

class FriendRequest(models.Model):
    type = models.CharField(max_length=200, default="follow")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    summary = models.CharField(max_length=200)
    actor = models.ForeignKey('Profile', related_name='%(class)s_author', on_delete=models.CASCADE,)
    object = models.ForeignKey('Profile', related_name='%(class)s_object', on_delete=models.CASCADE,)

# Inbox liked
class Like(models.Model):
    type = models.CharField(max_length=200, default="like")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)

    # who likes it
    author = models.ForeignKey('Profile', related_name='%(class)s_author', on_delete=models.CASCADE,)
    # URL of the likes

    context = models.CharField(max_length=200, default="Like")
    # likes items title, post title
    summary = models.CharField(max_length=200, default="Like")
    # Likes obj, ie post
    object = models.CharField(max_length=200, default="Like")

# People's liked items
class Liked(models.Model):
    type = models.CharField(max_length=200, default="liked")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    items = models.ManyToManyField('Like', blank=True)
