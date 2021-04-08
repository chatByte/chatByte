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
        self.user = User.objects.create_user(id=1,email='testuser@123.com',username='1')
        self.post = Post.objects.create(id=2, title='abc', description='test_des', author=self.user.profile)
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
        updatePost(self.post.id, 'abcd', '', '', '', '', '', '', '')
        filter_after = Post.objects.filter(title='abc')
        list_after = list(filter_after)
        # print("after id:", filter_after[0].ID)
        # print("len abc:", len(filter_after))
        after = list(filter_after)
        new_after = list(Post.objects.filter(title='abcd'))
        # print("new len:", len(new_after))
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
        # print("old id:", filter_before[0].ID)
        # print("len:", len(list_before))
        editPostDescription(self.post.id, 'new_des')
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
        self.post_id = 3
        self.comment = Comment.objects.create(id="5", 
                                              author=self.user.profile, 
                                              comment="test comment",
                                              contentType='text',
                                              parent_post=self.post
                                              )
        return super().setUp()
    
    def test_get_profile(self):
        """
        Ensure we can get an author's profile.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/author/1/'
        response = self.client.get(url,  **{'HTTP_X_SERVER': host})
        # print(response.content)
        user_json = {"type": "author", "id": host + "author/1", "host": None, "displayName": "test", "url": None, "github": None}
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
        # print(response.content)
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
        url = '/author/1/posts/'
        response = self.client.get(url,  **{'HTTP_X_SERVER': host})
        self.assertEqual(response.status_code, 200)
    
    def test_post_posts(self):
        """
        Ensure we can create a post for an author.
        """
        self.client.login(username=self.username, password=self.password)
        url = '/author/1/posts/'
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
            "comment_url": "1",
            "comments": [],
            "published": "2021-03-26T19:04:53Z",
            "visibility": "public",
            "unlisted": "false"
        }
        response = self.client.post(url, post_json, format='json',  **{'HTTP_X_SERVER': host})
        # print(response.content)
        self.assertEqual(response.status_code, 201)
#         # self.assertJSONEqual(
#         #     str(response.content, encoding='utf8'),
#         #     post_json
#         # )
    
    # def test_get_post(self):
    #     """
    #     Ensure we can update an author's post.
    #     """
    #     self.client.login(username=self.username, password=self.password)
    #     self.user.profile.timeline.add(self.post)
    #     url = '/author/1/posts/' + str(self.post_id) + '/'
    #     print(url)
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    
#     def test_post_post(self):
#         """
#         Ensure we can update an author's post.
#         """
#         self.client.login(username=self.username, password=self.password)
#         url = '/chat/author/1/posts/' + str(self.post_id) + '/'
#         post_json = {
#             "type": "post",
#             "id": self.post_id,
#             "title": "ffffffffffffffffffffffffffffff",
#             "source": "https://chatbyte.herokuapp.com/",
#             "origin": "https://chatbyte.herokuapp.com/",
#             "description": "asdf",
#             "contentType": "text",
#             "content": "asdf",
#             "author": {
#                 "type": "author",
#                 "id": "1",
#                 "host": None,
#                 "displayName": "test",
#                 "url": None,
#                 "github": None
#             },
#             "categories": "text/plain",
#             "count": 1,
#             "size": 1,
#             "commentsPage": "1",
#             "comments": [],
#             "published": "2021-03-26T19:04:53Z",
#             "visibility": "public",
#             "unlisted": "false"
#         }
#         response = self.client.post(url, post_json, format='json')
#         # print(response.content)
#         self.assertEqual(response.status_code, 201)

#     def test_delete_post(self):
#         """
#         Ensure we can delete an author's post.
#         """
#         self.client.login(username=self.username, password=self.password)
#         url = str(self.post_id)
#         response = self.client.delete(url)
#         # print(response.content)
#         self.assertEqual(response.status_code, 204)
    
#     def test_put_post(self):
#         """
#         Ensure we can delete an author's post.
#         """
#         self.client.login(username=self.username, password=self.password)
#         url = '/chat/author/1/posts/asdf/'
#         post_json = {
#             "type": "post",
#             "id": "asdf",
#             "title": "ffffffffffffffffffffffffffffff",
#             "source": "https://chatbyte.herokuapp.com/",
#             "origin": "https://chatbyte.herokuapp.com/",
#             "description": "asdf",
#             "contentType": "text",
#             "content": "asdf",
#             "author": {
#                 "type": "author",
#                 "id": "1",
#                 "host": None,
#                 "displayName": "test",
#                 "url": None,
#                 "github": None
#             },
#             "categories": "text/plain",
#             "count": 1,
#             "size": 1,
#             "commentsPage": "1",
#             "comments": [],
#             "published": "2021-03-26T19:04:53Z",
#             "visibility": "public",
#             "unlisted": "false"
#         }
#         response = self.client.put(url, post_json, format='json')
#         # print(response.content)
#         self.assertEqual(response.status_code, 201)
    
    def test_get_comments(self):
        self.client.login(username=self.username, password=self.password)
        url = '/author/1/posts/3/comments/'
        response = self.client.get(url, **{'HTTP_X_SERVER': host})
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_post_comments(self):
        self.client.login(username=self.username, password=self.password)
        url = '/author/'+ str(self.user.id) +'/posts/3/comments/'
        print("*****post_id:", self.post.id)
        
        comment_json = {
            "type": "comment",
            "id": host + url + '4',
            "author": {
                "type": "author",
                "id": str(self.user.id),
                "host": None,
                "displayName": "test",
                "url": None,
                "github": None
            },
            "comment": "test comment",
            "contentType": "text",
            "published": "2021-03-26T19:04:53Z"
        }
        response = self.client.post(url, comment_json, format='json',  **{'HTTP_X_SERVER': host})
        print(response.content)
        self.assertEqual(response.status_code, 201)

    # def test_delete_comments(self):
    #     # TODO
    #     self.client.login(username=self.username, password=self.password)
    #     url = '/author/1/posts/3/comments/5'
    #     response = self.clients.delete(url, **{'Origin': host})
        

# TODO: friends
# TODO: inbox test


