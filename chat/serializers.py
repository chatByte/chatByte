from rest_framework import serializers


import uuid
import django
from django.contrib.auth.models import User

from .models import *


# class CommentSerializer(serializers.Serializer):
#     # title = serializers.CharField(max_length=120)
#     # description = serializers.CharField()
#     # body = serializers.CharField()
#     # author_id = serializers.IntegerField()


#     TYPE = models.CharField(max_length=200, default="comment")
#     ID = serializers.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
#     AUTHOR = serializers.ForeignKey(User, on_delete=serializers.CASCADE,)
#     COMMENT = serializers.TextField()
#     CONTENT_TYPE = serializers.CharField(max_length=200)
#     PUBLISHED = serializers.DateTimeField(default=django.utils.timezone.now)

#     def create(self, validated_data):
#         """
#         Create and return a new `COMMENT` instance, given the validated data.
#         """
#         return Comment.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `COMMENT` instance, given the validated data.
#         """
#       instance.TYPE = validated_data.get('TYPE', instance.TYPE)
#       instance.ID = validated_data.get('ID', instance.ID)
#         instance.AUTHOR = validated_data.get('AUTHOR', instance.AUTHOR)
#         instance.COMMENT = validated_data.get('COMMENT', instance.COMMENT)
#         instance.CONTENT_TYPE = validated_data.get('CONTENT_TYPE', instance.CONTENT_TYPE)
#         instance.PUBLISHED = validated_data.get('PUBLISHED', instance.PUBLISHED)

#         instance.save()
#         return instance



# class PostSerializer(serializers.Serializer):

#   TYPE = models.CharField(max_length=200, default="post")
#   ID = serializers.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
#     TITLE = serializers.TextField()
#     SOURCE = serializers.CharField(max_length=200)
#     ORIGIN = serializers.CharField(max_length=200)
#     DESCRIPTION = serializers.TextField()
#     CONTENT_TYPE = serializers.CharField(max_length=200)
#     CONTENT = serializers.TextField()
#     AUTHOR = serializers.ForeignKey(User, on_delete=models.CASCADE,)
#     CATEGORIES = serializers.CharField(max_length=200)
#     COUNT = serializers.IntegerField()
#     SIZE = serializers.IntegerField()
#     COMMENTS_FIRST_PAGE = serializers.CharField(max_length=200)
#     COMMENTS = serializers.ManyToManyField('Comment', blank=True)
#     PUBLISHED = serializers.DateTimeField(default=django.utils.timezone.now)

#     VISIBILITY = serializers.CharField(max_length=50)
#     UNLISTED = serializers.CharField(max_length=50, default='false', editable=False)



#     # title = serializers.CharField(max_length=120)
#     # description = serializers.CharField()
#     # body = serializers.CharField()
#     # author_id = serializers.IntegerField()

#     def create(self, validated_data):
#         """
#         Create and return a new `POST` instance, given the validated data.
#         """
#         return Post.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `POST` instance, given the validated data.
#         """
#       instance.TYPE = validated_data.get('TYPE', instance.TYPE)

#         instance.ID = validated_data.get('ID', instance.ID)
#         instance.TITLE = validated_data.get('TITLE', instance.TITLE)
#         instance.SOURCE = validated_data.get('SOURCE', instance.SOURCE)
#         instance.ORIGIN = validated_data.get('ORIGIN', instance.ORIGIN)
#         instance.DESCRIPTION = validated_data.get('DESCRIPTION', instance.DESCRIPTION)
#         instance.CONTENT_TYPE = validated_data.get('CONTENT_TYPE', instance.CONTENT_TYPE)
#         instance.CONTENT = validated_data.get('CONTENT', instance.CONTENT)
#         instance.AUTHOR = validated_data.get('AUTHOR', instance.AUTHOR)
#         instance.CATEGORIES = validated_data.get('CATEGORIES', instance.CATEGORIES)
#         instance.COUNT = validated_data.get('COUNT', instance.COUNT)
#         instance.SIZE = validated_data.get('SIZE', instance.SIZE)
#         instance.COMMENTS_FIRST_PAGE = validated_data.get('COMMENTS_FIRST_PAGE', instance.COMMENTS_FIRST_PAGE)
#         instance.COMMENTS = validated_data.get('COMMENTS', instance.COMMENTS)
#         instance.PUBLISHED = validated_data.get('PUBLISHED', instance.PUBLISHED)
#         instance.VISIBILITY = validated_data.get('VISIBILITY', instance.VISIBILITY)
#         instance.UNLISTED = validated_data.get('UNLISTED', instance.UNLISTED)


#         instance.save()
#         return instance

class CommentSerializer(serializers.ModelSerializer):


    class Meta:
        model = Comment
        fields = ['type', 'id', 'author', 'comment', 'contentType', 'published']


class PostSerializer(serializers.ModelSerializer):


    class Meta:

        model = Post
        fields = ['type','id', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'size', 'commentsPage', 'comments', 'published', 'visibility', 'unlisted'  ]
        

class ProfileSerializer(serializers.ModelSerializer):

        # TODO
      class Meta:

        model = Profile
        fields = ['type','id', 'host', 'displayName', 'url', 'github']