from django.db import models
import uuid
import django

# Create your models here.
class User(models.Model):
    # for authorization only
    ID = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    USERNAME = models.CharField(max_length=50)
    PASSWORD = models.CharField(max_length=50)

class Author(models.Model):
    ID = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    HOST = models.CharField(max_length=200)
    DISPLAY_NAME = models.CharField(max_length=200, unique=True)
    URL = models.CharField(max_length=200)
    GITHUB = models.CharField(max_length=200)
    FRIENDS = models.ManyToManyField("self", blank=True)
    FOLLOWERS = models.ManyToManyField("self", blank=True)
    TIMELINE = models.ManyToManyField("Post", blank=True)
    FRIEND_REQUESTS = models.ManyToManyField("self", blank=True)

class Comment(models.Model):
    ID = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    AUTHOR = models.ForeignKey('Author', on_delete=models.DO_NOTHING,)
    COMMENT = models.TextField()
    CONTENT_TYPE = models.CharField(max_length=200)
    PUBLISHED = models.DateTimeField(default=django.utils.timezone.now)

class Post(models.Model):
    ID = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    TITLE = models.TextField()
    SOURCE = models.CharField(max_length=200)
    ORIGIN = models.CharField(max_length=200)
    DESCIPTION = models.TextField()
    CONTENT_TYPE = models.CharField(max_length=200)
    CONTENT = models.TextField()
    AUTHOR = models.ForeignKey('Author', on_delete=models.DO_NOTHING,)
    CATEGORIES = models.CharField(max_length=200)
    COMMENTS_NO = models.IntegerField()
    PAGE_SIZE = models.IntegerField()
    COMMENTS_FIRST_PAGE = models.CharField(max_length=200)
    COMMENTS = models.ForeignKey('Comment', on_delete=models.DO_NOTHING, blank=True)
    PUBLISHED = models.DateTimeField(default=django.utils.timezone.now)

    PUBLIC = 'public'
    FRIEND = 'friend'
    VISIBILITY_CHOICES = [ (PUBLIC, 'Public'), (FRIEND, 'Friend'), ]
    VISIBILITY = models.CharField(max_length=6, choices=VISIBILITY_CHOICES, default=PUBLIC,)
    UNLISTED = models.CharField(max_length=5, default='false', editable=False)

