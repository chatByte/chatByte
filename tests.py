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

# Create your tests here.

# class AuthorTestCase(TestCase):
#     def setUp(self):
#         author1 = Author.objects.create(HOST='test', DISPLAY_NAME='test', URL='test', GITHUB='test')
#         author2 = Author.objects.create(HOST='testfriend', DISPLAY_NAME='testfriend', URL='testfriend', GITHUB='testfriend')
#         post = Post.objects.create(TITLE='title', SOURCE='test', ORIGIN='origin', DESCIPTION='description', CONTENT_TYPE='content_type', CONTENT='content' \
#             , AUTHOR=author1, CATEGORIES='categories', COMMENTS_NO=0, PAGE_SIZE=0, COMMENTS_FIRST_PAGE='', VISIBILITY='visibility')
#         author1.TIMELINE.add(post)

#     def test_getTimeline(self):
#         # print('timeline_all:', Author.objects.filter(DISPLAY_NAME='test')[0].TIMELINE.all())
#         # print('time line get:', getTimeline('test'))
#         self.assertEqual(list(getTimeline('test')), list(Author.objects.filter(DISPLAY_NAME='test')[0].TIMELINE.all()))

#     def test_getAuthor(self):
#         self.assertEqual(getAuthor('test'), Author.objects.filter(DISPLAY_NAME='test')[0])

#     def test_createAuthor(self):
#         list_before = list(Author.objects.filter(DISPLAY_NAME='testAuthor'))
#         self.assertEqual(len(list_before), 0)
#         createAuthor('testHost','testAuthor','','')
#         list_after = list(Author.objects.filter(DISPLAY_NAME='testAuthor'))
#         print("after create Author:", list_after)
#         self.assertEqual(len(list_after), 1)

#     def test_updateAuthor(self):
#         author = Author.objects.filter(DISPLAY_NAME='test')[0]
#         self.assertEqual(author.URL, 'test')
#         updateAuthor('test','testAuthor','','')
#         author = Author.objects.filter(DISPLAY_NAME='test')[0]
#         self.assertEqual(author.URL, '')

#     def test_deleteAuthor(self):
#         list_before = list(Author.objects.filter(DISPLAY_NAME='test'))
#         deleteAuthor('test')
#         list_after = list(Author.objects.filter(DISPLAY_NAME='test'))
#         self.assertEqual(len(list_before) - len(list_after), 1)

class PostTestCase(TestCase):
    def setUp(self):
        self.post = Post.objects.create(id=2, title='abc', description='test_des')
        # Post.objects.create(ID=1)
        # Author.objects.create(HOST='test', DISPLAY_NAME='test', URL='test', GITHUB='test')


    def test_createPost(self):
        list_before = list(Post.objects.filter(title='test_title'))
        user = User.objects.create(email='abc@123.com')
        # timeline_before = list(author.TIMELINE.all())

        self.assertTrue(createPost('test_title','test','test','abc','text','content', user.profile,'',''))
        list_after = list(Post.objects.filter(title='test_title'))
        # author_after = Author.objects.filter(DISPLAY_NAME='test')[0]
        # timeline_after = list(author_after.TIMELINE.all())
        self.assertEqual(len(list_after) - len(list_before), 1)
        # self.assertEqual(len(timeline_after) - len(timeline_before), 1)


    def test_updatePost(self):
        filter_before = Post.objects.filter(title='abc')
        list_before = list(filter_before)
        # print("old id:", filter_before[0].ID)
        # print("len:", len(list_before))
        updatePost(2, 'abcd', '', '', '', '', '', '', '')
        filter_after = Post.objects.filter(title='abc')
        list_after = list(filter_after)
        # print("after id:", filter_after[0].ID)
        # print("len abc:", len(filter_after))
        after = list(filter_after)
        new_after = list(Post.objects.filter(title='abcd'))
        # print("new len:", len(new_after))
        self.assertEqual(len(after) - len(list_before), -1)


    def test_deletePost(self):
        list_before = list(Post.objects.filter(id=2))
        deletePost(2)
        list_after = list(Post.objects.filter(id=2))
        self.assertEqual(len(list_before) - len(list_after), 1)

    def test_getPost(self):
        self.assertEqual(getPost(2), Post.objects.get(id=2))

    def test_editPostDescription(self):
        filter_before = Post.objects.filter(description='test_des')
        list_before = list(filter_before)
        # print("old id:", filter_before[0].ID)
        # print("len:", len(list_before))
        editPostDescription(2, 'new_des')
        filter_after = Post.objects.filter(description='test_des')
        list_after = list(filter_after)
        # print("after id:", filter_after[0].ID)
        # print("len abc:", len(filter_after))
        after = list(filter_after)
        new_after = list(Post.objects.filter(description='new_des'))
        # print("new len:", len(new_after))
        self.assertEqual(len(after) - len(list_before), -1)


class CommentTestCase(TestCase):
    def setUp(self):
        # self.profile = Profile.objects.create(user=User, HOST='', DISPLAY_NAME='testProfile')
        # self.author = Author.objects.create(HOST='test', DISPLAY_NAME='test', URL='test', GITHUB='test')
        self.comment = Comment.objects.create(id=1, comment='test')
        self.post = Post.objects.create(id=2, title='abc')

    def test_createComment(self):
        # self.comment = createComment(self.author, 'comment test', 'text')
        list_before = list(Comment.objects.filter(comment='comment test'))
        comments_before = list(self.post.comments.all())

        user = User.objects.create(email='abc@123.com')
        self.assertTrue(createComment(user.profile, '2','comment test', 'text'))

        comments_after = list(self.post.comments.all())

        list_after = list(Comment.objects.filter(comment='comment test'))
        self.assertEqual(len(list_after) - len(list_before), 1)
        self.assertEqual(len(comments_after) - len(comments_before), 1)

    def test_updateComment(self):
        # new_comment = Comment.objects.create(AUTHOR=self.author, COMMENT='update comment test', CONTENT_TYPE='text')
        self.assertEqual(updateComment(1), True)

    def test_deleteComment(self):
        list_before = list(Comment.objects.filter(id=1))
        deleteComment(1)
        # new_comment = Comment.objects.create(AUTHOR=self.author, COMMENT='delete comment test', CONTENT_TYPE='text')
        list_after = list(Comment.objects.filter(id=1))
        self.assertEqual(len(list_after) - len(list_before), -1)

    def test_getComment(self):
        self.assertEqual(list(getComments(2).all()), list(self.post.comments.all()))


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
        self.post = Post.objects.create(title='test_title',
                                        source='test',
                                        origin='test',
                                        description='abc',
                                        contentType='text',
                                        content='content', 
                                        author=self.user.profile,
                                        categories='',
                                        count=0,
                                        size=0,
                                        commentsPage='0',
                                        visibility='public')
        self.post_id = self.post.id
        return super().setUp()
    
    def test_get_profile(self):
        """
        Ensure we can get an author's profile.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/chat/author/1/'
        response = self.client.get(url)
        user_json = {"type": "author", "id": "1", "host": None, "displayName": "test", "url": None, "github": None}
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
        url = '/chat/author/1/'
        user_json = {
            "type": "author",
            "id": "2",
            "host": "https://chatbyte.herokuapp.com/chat/author/2/",
            "displayName": "test",
            "url": "https://chatbyte.herokuapp.com/chat/author/2/profile/",
            "github": "https://github.com/Jeremy0818"
        }
        response = self.client.post(url, user_json, format='json')
        # print(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            user_json
        )

    def test_update_profile(self):
        """
        Ensure we can update an author's profile.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/chat/author/1/'
        user_json = {
            "type": "author",
            "id": "2",
            "host": "https://chatbyte.herokuapp.com/chat/author/2/",
            "displayName": "test",
            "url": "https://chatbyte.herokuapp.com/chat/author/2/profile/",
            "github": "https://github.com/Jeremy0818"
        }
        response = self.client.post(url, user_json, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            user_json
        )
    
    def test_get_posts(self):
        """
        Ensure we can update an author's posts.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/chat/author/1/posts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_posts(self):
        """
        Ensure we can create a post for an author.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/chat/author/1/posts/'
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
                "host": None,
                "displayName": "test",
                "url": None,
                "github": None
            },
            "categories": "text/plain",
            "count": 1,
            "size": 1,
            "commentsPage": "1",
            "comments": [],
            "published": "2021-03-26T19:04:53Z",
            "visibility": "public",
            "unlisted": "false"
        }
        response = self.client.post(url, post_json, format='json')
        # print(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            post_json
        )
    
    def test_get_post(self):
        """
        Ensure we can update an author's post.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/chat/author/1/posts/' + str(self.post_id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
    def test_post_post(self):
        """
        Ensure we can update an author's post.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/chat/author/1/posts/' + str(self.post_id) + '/'
        post_json = {
            "type": "post",
            "id": self.post_id,
            "title": "ffffffffffffffffffffffffffffff",
            "source": "https://chatbyte.herokuapp.com/",
            "origin": "https://chatbyte.herokuapp.com/",
            "description": "asdf",
            "contentType": "text",
            "content": "asdf",
            "author": {
                "type": "author",
                "id": "1",
                "host": None,
                "displayName": "test",
                "url": None,
                "github": None
            },
            "categories": "text/plain",
            "count": 1,
            "size": 1,
            "commentsPage": "1",
            "comments": [],
            "published": "2021-03-26T19:04:53Z",
            "visibility": "public",
            "unlisted": "false"
        }
        response = self.client.post(url, post_json, format='json')
        # print(response.content)
        self.assertEqual(response.status_code, 201)

    def test_delete_post(self):
        """
        Ensure we can delete an author's post.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/chat/author/1/posts/' + str(self.post_id) + '/'
        response = self.client.delete(url)
        # print(response.content)
        self.assertEqual(response.status_code, 204)
    
    def test_put_post(self):
        """
        Ensure we can delete an author's post.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/chat/author/1/posts/asdf/'
        post_json = {
            "type": "post",
            "id": "asdf",
            "title": "ffffffffffffffffffffffffffffff",
            "source": "https://chatbyte.herokuapp.com/",
            "origin": "https://chatbyte.herokuapp.com/",
            "description": "asdf",
            "contentType": "text",
            "content": "asdf",
            "author": {
                "type": "author",
                "id": "1",
                "host": None,
                "displayName": "test",
                "url": None,
                "github": None
            },
            "categories": "text/plain",
            "count": 1,
            "size": 1,
            "commentsPage": "1",
            "comments": [],
            "published": "2021-03-26T19:04:53Z",
            "visibility": "public",
            "unlisted": "false"
        }
        response = self.client.put(url, post_json, format='json')
        # print(response.content)
        self.assertEqual(response.status_code, 201)
    
    def test_get_comments(self):
        # TODO
        self.client.login(username=self.username, password=self.password)
        url = '/chat/author/1/posts/asdf/'

    def test_post_comments(self):
        # TODO
        self.client.login(username=self.username, password=self.password)
        url = '/chat/author/1/posts/asdf/'

    def test_delete_comments(self):
        # TODO
        self.client.login(username=self.username, password=self.password)
        url = '/chat/author/1/posts/asdf/'