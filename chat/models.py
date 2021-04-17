from django.db import models
import uuid
import django
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.


"""
profile model, saved in batabase
"""
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

    liked = models.OneToOneField('Liked', on_delete=models.CASCADE, null=True, blank=True)

    def __unicode__(self): # for Python 2
        return self.user.username

    # design for local method
    class Meta:
        managed = False


"""
Comment model, saved in batabase
"""
class Comment(models.Model):
    type = models.CharField(max_length=200, default="comment")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)

    author = models.ForeignKey('Profile', on_delete=models.CASCADE,)

    comment = models.TextField()
    contentType = models.CharField(max_length=200)
    published = models.DateTimeField(default=django.utils.timezone.now)
    likes = models.ManyToManyField('Like', blank=True)
    # # the father of Comeent is POST
    parent_post = models.ForeignKey("Post", on_delete= models.CASCADE, null=True, blank=True)


"""
Post model, saved in batabase
"""
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
    # categories = ArrayField(
    #     models.CharField(max_length=200, blank=True),
    #     size=200,
    # )
    categories = models.CharField(max_length=200, blank=True)
    count = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    comment_url = models.CharField(max_length=200, blank=True)
    comments = models.ManyToManyField('Comment', blank=True)
    # published date
    published = models.DateTimeField(default=django.utils.timezone.now)
    visibility = models.CharField(max_length=50)
    unlisted = models.BooleanField(default=False)
    likes = models.ManyToManyField('Like', blank=True)

"""
Post inbox model, saved in batabase
"""
class PostInbox(models.Model):
    type = models.CharField(max_length=200, default="inbox", blank=True)
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    author = models.CharField(max_length=200, blank=True, null=True)
    items = models.ManyToManyField('Post', blank=True)


"""
Inbox model, saved in batabase
"""
class Inbox(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    post_inbox = models.OneToOneField('PostInbox', on_delete=models.CASCADE, null=True, blank=True)
    like_inbox = models.ManyToManyField('Like', blank=True)
    friend_requests = models.ManyToManyField('FriendRequest', blank=True)


"""
Followed model, saved in batabase
"""
class Follower(models.Model):
    # get a list of authors who are their followers
    type = models.CharField(max_length=200, default="followers")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    # Here items are Authors , which is Profiles
    items = models.ManyToManyField('Profile', related_name='%(class)s_followers_items', blank=True)


"""
Friedn request model, saved in batabase
"""
class FriendRequest(models.Model):
    type = models.CharField(max_length=200, default="follow")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    summary = models.CharField(max_length=200)
    actor = models.ForeignKey('Profile', related_name='%(class)s_author', on_delete=models.CASCADE,)
    object = models.ForeignKey('Profile', related_name='%(class)s_object', on_delete=models.CASCADE,)


"""
Like model, saved in batabase
"""
# Inbox liked
class Like(models.Model):
    type = models.CharField(max_length=200, default="like")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)

    # who likes it
    author = models.ForeignKey('Profile', related_name='%(class)s_author', on_delete=models.CASCADE,)
    # URL of the likes

    context = models.CharField(max_length=200, default="", blank=True)
    # likes items title, post title
    summary = models.CharField(max_length=200, default="")
    # Likes obj, ie post
    object = models.CharField(max_length=200, default="")

# People's liked items
class Liked(models.Model):
    type = models.CharField(max_length=200, default="liked")
    id = models.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    items = models.ManyToManyField('Like', blank=True)


"""
Nodes model, saved in batabase, deisgn for connection
"""
class Node(models.Model):
    username = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200,  blank=True)
    origin = models.CharField(max_length=200,  blank=True)