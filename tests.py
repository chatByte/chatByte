from django.test import TestCase
from chat.models import Post, Comment, Profile
from django.contrib.auth.models import User
from chat.backend import *
# Create your tests here.

# class ActorTestCase(TestCase):

#     def setUp(self):
#         # set up
#         Actor.objects.create(USERNAME='test', PASSWORD='123')
#         Actor.objects.create(USERNAME='testfriend', PASSWORD='123')
#         # User.objects.create(USERNAME='testfriend', PASSWORD='123')

#     def test_validActor(self):
#         self.assertEqual(validActor('test123', '123'), False)
#         self.assertEqual(validActor('test', '123'), True)

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

#     def test_addFriend(self):
#         list_before = list(Author.objects.filter(DISPLAY_NAME='test')[0].FRIENDS.all())
#         # print(list_before)
#         addFriend('test', 'testfriend')
#         list_after = list(Author.objects.filter(DISPLAY_NAME='test')[0].FRIENDS.all())
#         # print("list_after",list_after)
#         self.assertEqual(len(list_after) - len(list_before), 1)

#     def test_getFriends(self):
#         self.assertEqual(list(getFriends('test')), list(Author.objects.filter(DISPLAY_NAME='test')[0].FRIENDS.all()))

#     def test_deleteFriend(self):
#         addFriend('test', 'testfriend')
#         list_before = list(Author.objects.filter(DISPLAY_NAME='test')[0].FRIENDS.all())
#         deleteFriend('test', 'testfriend')
#         list_after = list(Author.objects.filter(DISPLAY_NAME='test')[0].FRIENDS.all())
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
