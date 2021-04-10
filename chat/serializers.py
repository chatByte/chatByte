from rest_framework import serializers, pagination
from django.http import JsonResponse
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
      class Meta:
        model = Profile
        fields = ['type','id', 'host', 'displayName', 'url', 'github']
        extra_kwargs = {
            'displayName': {'validators': []},
            'id': {'validators': []},
        }

class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    class Meta:
        model = Comment
        fields = ['type', 'id', 'author', 'comment', 'contentType', 'published']
        extra_kwargs = {
            'id': {'validators': []},
        }
    
    def update(self, instance, validated_data):
        print("---------***--------------")
        print(validated_data)
        instance.type = validated_data.get('type', instance.type)
        instance.id = validated_data.get('id', instance.id)
        author_ser = ProfileSerializer(instance.author, data=validated_data.get('author', instance.author))
        if author_ser.is_valid():
            instance.author = author_ser.save()
        instance.comment = validated_data.get('comment', instance.comment)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.published = validated_data.get('published', instance.published)
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = ['type','id', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'categories', 'count', 'size', 'comment_url', 'comments', 'published', 'visibility', 'unlisted'  ]
    
    def create(self, validated_data):
        print("---------***********--------------")
        comments_data = validated_data.pop('comments')
        author = validated_data.pop('author')
        print(author)
        # try: 
        #     author = Profile.objects.get(id=author_data['id'])
        # except:
        #     author = Profile.objects.create(**author_data)
        print("---------******************--------------")
        post = Post.objects.create(author=author, **validated_data)
        print("---------******************************--------------")
        for comment_data in comments_data:
            author_data = comment_data.pop('author')
            try: 
                com_author = Profile.objects.get(id=author_data['id'])
            except:
                com_author = Profile.objects.create(**author_data)
            print("---------********************************--------------")
            comment = Comment.objects.create(author=com_author, **comment_data)
            post.comments.add(comment)
        post.save()
        return post
    
    def update(self, instance, validated_data):
        print("---------***--------------")
        print(validated_data)
        instance.type = validated_data.get('type', instance.type)
        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.source = validated_data.get('source', instance.source)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.description = validated_data.get('description', instance.description)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.content = validated_data.get('content', instance.content)
        author_ser = ProfileSerializer(instance.author, data=validated_data.get('author', instance.author))
        if author_ser.is_valid():
            instance.author = author_ser.save()
        instance.categories = validated_data.get('categories', instance.categories)
        instance.count = validated_data.get('count', instance.count)
        instance.size = validated_data.get('size', instance.size)
        instance.comment_url = validated_data.get('comment_url', instance.comment_url)
        comments_data = validated_data.get('comments')
        comments = (instance.comments).all()
        comments = list(comments)
        for comment_data in comments_data:
            comment = comments.pop(0)
            comment_ser = CommentSerializer(comment, data=comment_data)
            if comment_ser.is_valid():
                comment_ser.save()
        instance.published = validated_data.get('published', instance.published)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.unlisted = validated_data.get('unlisted', instance.unlisted)
        instance.save()
        return instance
        

class PostInboxSerializer(serializers.ModelSerializer):
    items = PostSerializer(many=True)
    class Meta:
        model = PostInbox
        fields = ['type','author', 'items']

class FriendReuqestSerializer(serializers.ModelSerializer):
    actor = ProfileSerializer(read_only=True)
    object = ProfileSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['type','id', 'summary', 'actor', 'object']


class LikeSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['type','id', 'summary', 'author', 'object', 'context']

class FollowerSerializer(serializers.ModelSerializer):
    items = ProfileSerializer(many=True)
    class Meta:
        model = Follower
        fields = ['type', 'items']

class LikedSerializer(serializers.ModelSerializer):
    items = LikeSerializer(many=True)
    class Meta:
        model = Liked
        fields = ['type', 'items']

# class CommentCustomPagination(pagination.PageNumberPagination):
#     def get_paginated_response(self, data):
#         return JsonResponse({
#             'next': self.get_next_link(),
#             'previous': self.get_previous_link(),
#             'count': self.page.paginator.count,
#             'comments': data
#         }, safe=False)

# class PostCustomPagination(pagination.PageNumberPagination):
#     def get_paginated_response(self, data):
#         return JsonResponse({
#             'next': self.get_next_link(),
#             'previous': self.get_previous_link(),
#             'count': self.page.paginator.count,
#             'posts': data
#         }, safe=False)
