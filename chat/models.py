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

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    HOST = models.CharField(max_length=200, null=True)
    DISPLAY_NAME = models.CharField(max_length=200, unique=True, null=True)
    URL = models.CharField(max_length=200, null=True)
    GITHUB = models.CharField(max_length=200, null=True)

    FRIENDS = models.ManyToManyField(User, related_name='%(class)s_friends', blank=True)
    FOLLOWERS = models.ManyToManyField(User, related_name='%(class)s_followers', blank=True)
    TIMELINE = models.ManyToManyField("Post", blank=True)
    FRIEND_REQUESTS = models.ManyToManyField(User, related_name='%(class)s_friend_requests', blank=True)

    def __unicode__(self): # for Python 2
        return self.user.username
    
    class Meta:
        managed = False

class Comment(models.Model):
    ID = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    AUTHOR = models.ForeignKey(User, on_delete=models.CASCADE,)
    COMMENT = models.TextField()
    CONTENT_TYPE = models.CharField(max_length=200)
    PUBLISHED = models.DateTimeField(default=django.utils.timezone.now)

class Post(models.Model):
    ID = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    TITLE = models.TextField()
    SOURCE = models.CharField(max_length=200)
    ORIGIN = models.CharField(max_length=200)
    DESCRIPTION = models.TextField()
    CONTENT_TYPE = models.CharField(max_length=200)
    CONTENT = models.TextField()
    AUTHOR = models.ForeignKey(User, on_delete=models.CASCADE,)
    CATEGORIES = models.CharField(max_length=200)
    COMMENTS_NO = models.IntegerField()
    PAGE_SIZE = models.IntegerField()
    COMMENTS_FIRST_PAGE = models.CharField(max_length=200)
    COMMENTS = models.ManyToManyField('Comment', blank=True)
    PUBLISHED = models.DateTimeField(default=django.utils.timezone.now)

    VISIBILITY = models.CharField(max_length=50)
    UNLISTED = models.CharField(max_length=50, default='false', editable=False)

# class Comment(models.Model):
#     ID = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
#     AUTHOR = models.ForeignKey('Author', on_delete=models.DO_NOTHING,)
#     COMMENT = models.TextField()
#     CONTENT_TYPE = models.CharField(max_length=200)
#     PUBLISHED = models.DateTimeField(default=django.utils.timezone.now)

# class Post(models.Model):
#     ID = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
#     TITLE = models.TextField()
#     SOURCE = models.CharField(max_length=200)
#     ORIGIN = models.CharField(max_length=200)
#     DESCIPTION = models.TextField()
#     CONTENT_TYPE = models.CharField(max_length=200)
#     CONTENT = models.TextField()
#     AUTHOR = models.ForeignKey('Author', on_delete=models.DO_NOTHING,)
#     CATEGORIES = models.CharField(max_length=200)
#     COMMENTS_NO = models.IntegerField()
#     PAGE_SIZE = models.IntegerField()
#     COMMENTS_FIRST_PAGE = models.CharField(max_length=200)
#     COMMENTS = models.ManyToManyField('Comment', blank=True)
#     PUBLISHED = models.DateTimeField(default=django.utils.timezone.now)

#     VISIBILITY = models.CharField(max_length=50)
#     UNLISTED = models.CharField(max_length=50, default='false', editable=False)

