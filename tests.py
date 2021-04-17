from chat.api import post_obj
from django.test import TestCase
from chat.models import Inbox, Post, Comment, PostInbox, Profile
from django.contrib.auth.models import User
from chat.backend import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
import json
from chat.signals import host

# Create your tests here.

class PostTestCase(TestCase):
    def setUp(self):
        self.liked = Liked.objects.create()
        self.profile = Profile.objects.create(liked=self.liked)
        self.user = User.objects.create_user(id=1,email='testuser@123.com',username='1')
        self.user.profile = self.profile
        self.post = Post.objects.create(id=2, title='abc', description='test_des', author=self.user.profile)
        # Post.objects.create(ID=1)
        # Author.objects.create(HOST='test', DISPLAY_NAME='test', URL='test', GITHUB='test')


    def test_createPost(self):
        list_before = list(Post.objects.filter(title='test_title'))
        user = User.objects.create(email='abc@123.com')
        # timeline_before = list(author.TIMELINE.all())
        self.assertTrue(createPost('test_title','test','test','abc','text','content', user.profile,'','', 'false'))
        list_after = list(Post.objects.filter(title='test_title'))
        # author_after = Author.objects.filter(DISPLAY_NAME='test')[0]
        # timeline_after = list(author_after.TIMELINE.all())
        self.assertEqual(len(list_after) - len(list_before), 1)
        # self.assertEqual(len(timeline_after) - len(timeline_before), 1)

    def test_updatePost(self):
        filter_before = Post.objects.filter(title='abc')
        list_before = list(filter_before)
        updatePost(self.post.id, 'abcd', '', 'text/plain', '')
        filter_after = Post.objects.filter(title='abc')
        list_after = list(filter_after)
        after = list(filter_after)
        new_after = list(Post.objects.filter(title='abcd'))
        self.assertEqual(len(after) - len(list_before), -1)


    def test_deletePost(self):
        list_before = list(Post.objects.filter(id=self.post.id))
        deletePost(self.post.id)
        list_after = list(Post.objects.filter(id=self.post.id))
        self.assertEqual(len(list_before) - len(list_after), 1)

    def test_getPost(self):
        self.assertEqual(getPost(self.post.id), Post.objects.get(id=self.post.id))

    def test_editPostDescription(self):
        filter_before = Post.objects.filter(description='test_des')
        list_before = list(filter_before)
        editPostDescription(self.post.id, 'new_des')
        filter_after = Post.objects.filter(description='test_des')
        list_after = list(filter_after)
        after = list(filter_after)
        new_after = list(Post.objects.filter(description='new_des'))
        self.assertEqual(len(after) - len(list_before), -1)

    def test_likePost(self):
        user_liked = self.user.profile.liked
        author_liked_before = list(self.user.profile.liked.items.all())
        post_likes_before = list(self.post.likes.all())
        likePost(self.post.id, self.user.profile.id)
        author_liked_after = list(self.user.profile.liked.items.all())
        post_likes_after = list(self.post.likes.all())
        self.assertEqual(len(author_liked_after) - len(author_liked_before), 1)
        self.assertEqual(len(post_likes_after) - len(post_likes_before), 1)

class CommentTestCase(TestCase):
    def setUp(self):
        # self.profile = Profile.objects.create(user=User, HOST='', DISPLAY_NAME='testProfile')
        # self.author = Author.objects.create(HOST='test', DISPLAY_NAME='test', URL='test', GITHUB='test')
        # self.user = User.objects.create_user(id=34,email='testuser@123.com',username='1')
        self.user = User.objects.create_user(id=1,email='testuser@123.com',username='1')
        self.post = Post.objects.create(id=2, title='abc', author=self.user.profile)

    def test_createComment(self):
        list_before = list(Comment.objects.filter(comment='comment test'))
        comments_before = list(self.post.comments.all())

        user = User.objects.create(email='abc@123.com')
        self.assertTrue(createComment(user.profile, self.post.id,'comment test', 'text'))

        comments_after = list(self.post.comments.all())

        list_after = list(Comment.objects.filter(comment='comment test'))
        self.assertEqual(len(list_after) - len(list_before), 1)
        self.assertEqual(len(comments_after) - len(comments_before), 1)

    def test_updateComment(self):
        # new_comment = Comment.objects.create(AUTHOR=self.author, COMMENT='update comment test', CONTENT_TYPE='text')
        user = User.objects.create(email='abc@123.com')
        comment  = Comment.objects.create(author=user.profile, comment="comment", contentType="content_type", parent_post=self.post)
        self.assertEqual(updateComment(comment.id), True)

    def test_deleteComment(self):
        user = User.objects.create(email='abc@123.com')
        comment = Comment.objects.create(author=user.profile, comment="comment", contentType="content_type", parent_post=self.post)
        list_before = list(Comment.objects.filter(id=comment.id))
        deleteComment(comment.id)
        # new_comment = Comment.objects.create(AUTHOR=self.author, COMMENT='delete comment test', CONTENT_TYPE='text')
        list_after = list(Comment.objects.filter(id=1))
        self.assertEqual(len(list_after) - len(list_before), -1)

    def test_getComment(self):
        self.assertEqual(list(getComments(self.post.id).all()), list(self.post.comments.all()))


class FriendsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(id=1,email='testuser@123.com',username='1')
        self.friend1 = User.objects.create_user(id=2,email='testfriend@123.com',username='2')
        self.user2 = User.objects.create_user(id=3,email='testuser@123.com',username='3')
        self.friend2 = User.objects.create_user(id=4,email='testfriend@123.com',username='4')
        self.user3 = User.objects.create_user(id=5,email='testuser@123.com',username='5')
        self.friend3 = User.objects.create_user(id=6,email='testfriend@123.com',username='6')
        self.friend4 = User.objects.create_user(id=7,email='testfriend@123.com',username='7')
        self.friend5 = User.objects.create_user(id=8,email='testfriend@123.com',username='8')
    # def setUp(self):
    #     self.user = User.objects.create(id=1,email='testuser@123.com')
    #     self.friend1 = User.objects.create(id=2,email='testfriend@123.com')
    #     self.friend1 = User.objects.create(id=3,email='testfriend@123.com')
    #     self.friend1 = User.objects.create(id=4,email='testfriend@123.com')


    def test_addFriend(self):
        list_before = list(self.user.profile.friends.all())
        addFriend(1, 2)
        list_after = list(self.user.profile.friends.all())
        self.assertEqual(len(list_after) - len(list_before), 1)

    def test_deleteFriend(self):
        addFriend(3, 4)
        list_before = list(self.user2.profile.friends.all())
        deleteFriend(3, 4)
        list_after = list(self.user2.profile.friends.all())
        self.assertEqual(len(list_after) - len(list_before), -1)

    def test_getFriend(self):
        addFriend(5,6)
        self.assertEqual(getFriend(5,6), self.friend3)

    # def test_getFriends(self):
    #     self.assertEqual(len(list(getFriends(7))), 0)
    #     addFriend(7, 8)
    #     self.assertEqual(len(list(getFriends(7))), 1)
    #
    # def test_addFriend(self):
    #     list_before = list(self.user.profile.FRIENDS.all())
    #     addFriend(1, 2)
    #     list_after = list(self.user.profile.FRIENDS.all())
    #     self.assertEqual(len(list_after) - len(list_before), 1)
    #     addFriend(1,3)
    #     addFriend(1,4)
    #     friend_list = list(self.user.profile.FRIENDS.all())
    #     for i in range(len(friend_list)):
    #         print(friend_list[i].id)

# -------------------------------------------------------------------------------------------------------------------------------
# API test cases
# -------------------------------------------------------------------------------------------------------------------------------

class AccountTests(APITestCase):
    def setUp(self) -> None:
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.post = Post.objects.create(id="3",
                                        title='test_title',
                                        source='test',
                                        origin='test',
                                        description='abc',
                                        contentType='text',
                                        content='content', 
                                        author=self.user.profile,
                                        categories='',
                                        count=0,
                                        size=0,
                                        comment_url='0',
                                        visibility='public')
        self.post1 = Post.objects.create(id="456",
                                        title='test_title',
                                        source='test',
                                        origin='test',
                                        description='abc',
                                        contentType='text',
                                        content='content', 
                                        author=self.user.profile,
                                        categories='',
                                        count=0,
                                        size=0,
                                        comment_url='0',
                                        visibility='public')
        self.post_id = 3
        self.comment = Comment.objects.create(id="5", 
                                              author=self.user.profile, 
                                              comment="test comment",
                                              contentType='text',
                                              parent_post=self.post
                                              )
        self.post.comments.add(self.comment)
        self.user.profile.timeline.add(self.post)
        self.user.profile.save()
        return super().setUp()
    
    def test_get_profile(self):
        """
        Ensure we can get an author's profile.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/author/1/'
        response = self.client.get(url,  **{'HTTP_X_SERVER': host})
        # print(response.content)
        user_json = {"type": "author", "id": host + "author/1", "host": 'https://chatbyte.herokuapp.com/', "displayName": "test", "url": '1', "github": None}
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            user_json
        )

    def test_update_profile(self):
        """
        Ensure we can update an author's profile.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/author/1/'
        user_json = {
            "type": "author",
            "id": host + "author/1",
            "host": "https://chatbyte.herokuapp.com/chat/author/2/",
            "displayName": "asdfasdfasdfadsfasd",
            "url": "https://chatbyte.herokuapp.com/chat/author/2/profile/",
            "github": "https://github.com/Jeremy0818"
        }
        response = self.client.post(url, user_json, format='json',  **{'HTTP_X_SERVER': host})
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            user_json
        )
    
    def test_get_posts(self):
        """
        Ensure we can update an author's posts.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/author/' + str(self.user.id) + '/posts/'
        response = self.client.get(url,  **{'HTTP_X_SERVER': host})
        self.assertEqual(response.status_code, 200)
    
    def test_post_posts(self):
        """
        Ensure we can create a post for an author.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/author/' + str(self.user.id) + '/posts/'
        post_json = {
            "type": "post",
            "id": "456456",
            "title": "fffffffffff",
            "source": "https://chatbyte.herokuapp.com/",
            "origin": "https://chatbyte.herokuapp.com/",
            "description": "asdf",
            "contentType": "text",
            "content": "asdf",
            "author": {
                "type": "author",
                "id": "1",
                "host": "https://chatbyte.herokuapp.com/",
                "displayName": "test",
                "url": "https://chatbyte.herokuapp.com/",
                "github": "https://chatbyte.herokuapp.com/"
            },
            "categories": "text/plain",
            "count": 1,
            "size": 1,
            "comment_url": "1",
            "comments": [],
            "published": "2021-03-26T19:04:53Z",
            "visibility": "public",
            "unlisted": "False"
        }
        response = self.client.post(url, post_json, format='json',  **{'HTTP_X_SERVER': host})
        self.assertEqual(response.status_code, 201)

    def test_delete_post(self):
        """
        Ensure we can delete an author's post.
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.delete(self.post1.id)
        self.assertEqual(response.status_code, 204)
    
    def test_put_post(self):
        """
        Ensure we can create a post with a specific id and content.
        """
        self.client.login(username=self.username, password=self.password)
        url = self.user.profile.id + '/posts/789789'
        post_json = {
            "type": "post",
            "id": "789789",
            "title": "fffffffffff",
            "source": "https://chatbyte.herokuapp.com/",
            "origin": "https://chatbyte.herokuapp.com/",
            "description": "asdf",
            "contentType": "text",
            "content": "asdf",
            "author": {
                "type": "author",
                "id": "1",
                "host": "https://chatbyte.herokuapp.com/",
                "displayName": "test",
                "url": "https://chatbyte.herokuapp.com/",
                "github": "https://chatbyte.herokuapp.com/"
            },
            "categories": "text/plain",
            "count": 1,
            "size": 1,
            "comment_url": "1",
            "comments": [],
            "published": "2021-03-26T19:04:53Z",
            "visibility": "public",
            "unlisted": "False"
        }
        response = self.client.put(url, post_json, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_get_comments(self):
        self.client.login(username=self.username, password=self.password)
        url = '/author/'+ str(self.user.id) +'/posts/3/comments'
        response = self.client.get(url, **{'HTTP_X_SERVER': host})
        self.assertEqual(response.status_code, 200)

    def test_post_comments(self):
        self.client.login(username=self.username, password=self.password)
        url = '/author/'+ str(self.user.id) +'/posts/3/comments'
        
        comment_json = {
            "content": "test comment",
            "contentType": "text"
        }
        response = self.client.post(url, comment_json, format='json',  **{'HTTP_X_SERVER': host, 'HTTP_X_REQUEST_USER': self.user.profile.id})
        self.assertEqual(response.status_code, 201)

    def test_get_friends(self):
        self.client.login(username=self.username, password=self.password)
        url = self.user.profile.id + "/friends/"
        response = self.client.get(url,  **{'HTTP_X_SERVER': host, 'HTTP_X_REQUEST_USER': self.user.profile.id})
        self.assertEqual(response.status_code, 200)

