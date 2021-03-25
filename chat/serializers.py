from rest_framework import serializers
from .models import Post, Comment, Profile

class PostSerializer(serializers.Serializer):
    ID = serializers.CharField(max_length=200, primary_key=True, unique=True, default=uuid.uuid4)
    TITLE = serializers.TextField()
    SOURCE = serializers.CharField(max_length=200)
    ORIGIN = serializers.CharField(max_length=200)
    DESCRIPTION = serializers.TextField()
    CONTENT_TYPE = serializers.CharField(max_length=200)
    CONTENT = serializers.TextField()
    AUTHOR = serializers.ForeignKey(User, on_delete=models.CASCADE,)
    CATEGORIES = serializers.CharField(max_length=200)
    COMMENTS_NO = serializers.IntegerField()
    PAGE_SIZE = serializers.IntegerField()
    COMMENTS_FIRST_PAGE = serializers.CharField(max_length=200)
    COMMENTS = serializers.ManyToManyField('Comment', blank=True)
    PUBLISHED = serializers.DateTimeField(default=django.utils.timezone.now)

    VISIBILITY = serializers.CharField(max_length=50)
    UNLISTED = serializers.CharField(max_length=50, default='false', editable=False)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.ID = validated_data.get('title', instance.title)
        instance.TITLE = validated_data.get('title', instance.title)
        instance.SOURCE = validated_data.get('title', instance.title)
        instance.ORIGIN = validated_data.get('title', instance.title)
        instance.DESCRIPTION = validated_data.get('title', instance.title)
        instance.CONTENT_TYPE = validated_data.get('title', instance.title)
        instance.CONTENT = validated_data.get('title', instance.title)
        instance.AUTHOR = validated_data.get('title', instance.title)
        instance.CATEGORIES = validated_data.get('title', instance.title)
        instance.COMMENTS_NO = validated_data.get('title', instance.title)
        instance.PAGE_SIZE = validated_data.get('title', instance.title)
        instance.COMMENTS_FIRST_PAGE = validated_data.get('title', instance.title)
        instance.COMMENTS = validated_data.get('title', instance.title)
        instance.PUBLISHED 
        instance.save()
        return instance