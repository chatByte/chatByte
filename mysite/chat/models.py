from django.db import models

# Create your models here.
class Author(models.Model):
    ID = models.CharField(max_length=200, primary_key=True)
    HOST = models.CharField(max_length=200)
    DISPLAY_NAME = models.CharField(max_length=200)
    URL = models.CharField(max_length=200)
    GITHUB = models.CharField(max_length=200)
    FRIENDS = models.ManyToManyField("self", null=True, blank=True)
    FOLLOWERS = models.ManyToManyField("self", null=True, blank=True)

class Comment(models.Model):
    ID = models.CharField(max_length=200, primary_key=True)
    AUTHOR = models.ForeignKey('Author', on_delete=models.DO_NOTHING,)
    COMMENT = models.TextField()
    CONTENT_TYPE = models.CharField(max_length=200)
    PUBLISHED = models.DateTimeField()

class Post(models.Model):
    ID = models.CharField(max_length=200, primary_key=True)
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
    COMMENTS = models.ForeignKey('Comment', on_delete=models.DO_NOTHING, null=True, blank=True)
    PUBLISHED = models.DateTimeField()

    PUBLIC = 'public'
    FRIEND = 'friend'
    VISIBILITY_CHOICES = [ (PUBLIC, 'Public'), (FRIEND, 'Friend'), ]
    VISIBILITY = models.CharField(max_length=6, choices=VISIBILITY_CHOICES, default=PUBLIC,)
    UNLISTED = models.CharField(max_length=7, default='false', editable=False)
