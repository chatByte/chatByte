from django.db import models
import uuid
import django
from django.contrib.auth.models import User

# Create your models here.
# class Actor(models.Model):
#     # for authorization only
#     ID = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
#     USERNAME = models.CharField(max_length=50, unique=True)
#     PASSWORD = models.CharField(max_length=50)


class Profile(models.Model):
    type = models.CharField(max_length=200, default="author")
    id = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    host = models.CharField(max_length=200, null=True)
    displayName = models.CharField(max_length=200, unique=True, null=True)
    url = models.CharField(max_length=200, null=True)
    github = models.CharField(max_length=200, null=True)

    friends = models.ManyToManyField(User, related_name='%(class)s_friends', blank=True)
    followers = models.ManyToManyField(User, related_name='%(class)s_followers', blank=True)
    timeline = models.ManyToManyField("Post", blank=True)
    friend_requests = models.ManyToManyField(User, related_name='%(class)s_friend_requests', blank=True)

    def __unicode__(self): # for Python 2
        return self.user.username
    
    class Meta:
        managed = False

class Comment(models.Model):
    type = models.CharField(max_length=200, default="comment")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    comment = models.TextField()
    contentType = models.CharField(max_length=200)
    published = models.DateTimeField(default=django.utils.timezone.now)

class Post(models.Model):
    type = models.CharField(max_length=200, default="post")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    title = models.TextField()
    source = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    description = models.TextField()
    contentType = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    categories = models.CharField(max_length=200)
    count = models.IntegerField()
    size = models.IntegerField()
    commentsPage = models.CharField(max_length=200)
    comments = models.ManyToManyField('Comment', blank=True)
    published = models.DateTimeField(default=django.utils.timezone.now)
    visibility = models.CharField(max_length=50)
    unlisted = models.CharField(max_length=50, default='false', editable=False)

class Inbox(models.Model):
    type = models.CharField(max_length=200, default="inbox")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    author = models.CharField(max_length=200)
    items = models.ManyToManyField('Post', blank=True)

class Followers(models.Model):
    type = models.CharField(max_length=200, default="followers")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    items = models.ManyToManyField(User, blank=True)

class FriendRequest(models.Model):
    type = models.CharField(max_length=200, default="follow")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    summary = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='%(class)s_author', on_delete=models.CASCADE,)
    object = models.ForeignKey(User, related_name='%(class)s_object', on_delete=models.CASCADE,)

class Like(models.Model):
    type = models.CharField(max_length=200, default="like")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    author = models.ForeignKey(User, related_name='%(class)s_author', on_delete=models.CASCADE,)
    context = models.CharField(max_length=200, default="Like")
    summary = models.CharField(max_length=200, default="Like")
    object = models.CharField(max_length=200, default="Like")

class Liked(models.Model):
    type = models.CharField(max_length=200, default="liked")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    items = models.ManyToManyField('Like', blank=True)

