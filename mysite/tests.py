from django.test import TestCase
from chat.models import Author, Post, Comment, Actor
from chat.api import *
# Create your tests here.

class ActorTestCase(TestCase):
    
    def setUp(self):
        # set up 
        Actor.objects.create(USERNAME='test', PASSWORD='123')
        Actor.objects.create(USERNAME='testfriend', PASSWORD='123')
        # User.objects.create(USERNAME='testfriend', PASSWORD='123')

    def test_validActor(self):
        self.assertEqual(validActor('test123', '123'), False)
        self.assertEqual(validActor('test', '123'), True)

class AuthorTestCase(TestCase):
    def setUp(self):
        author1 = Author.objects.create(HOST='test', DISPLAY_NAME='test', URL='test', GITHUB='test')
        author2 = Author.objects.create(HOST='testfriend', DISPLAY_NAME='testfriend', URL='testfriend', GITHUB='testfriend')
        post = Post.objects.create(TITLE='title', SOURCE='test', ORIGIN='origin', DESCIPTION='description', CONTENT_TYPE='content_type', CONTENT='content' \
            , AUTHOR=author1, CATEGORIES='categories', COMMENTS_NO=0, PAGE_SIZE=0, COMMENTS_FIRST_PAGE='', VISIBILITY='visibility')
        author1.TIMELINE.add(post)

    def test_getTimeline(self):
        # print('timeline_all:', Author.objects.filter(DISPLAY_NAME='test')[0].TIMELINE.all())
        # print('time line get:', getTimeline('test'))
        self.assertEqual(list(getTimeline('test')), list(Author.objects.filter(DISPLAY_NAME='test')[0].TIMELINE.all()))

    def test_getAuthor(self):
        self.assertEqual(getAuthor('test'), Author.objects.filter(DISPLAY_NAME='test')[0])

    def test_createAuthor(self):
        list_before = list(Author.objects.filter(DISPLAY_NAME='testAuthor'))
        self.assertEqual(len(list_before), 0)
        createAuthor('testHost','testAuthor','','')
        list_after = list(Author.objects.filter(DISPLAY_NAME='testAuthor'))
        print("after create Author:", list_after)
        self.assertEqual(len(list_after), 1)

    def test_updateAuthor(self):
        author = Author.objects.filter(DISPLAY_NAME='test')[0]
        self.assertEqual(author.URL, 'test')
        updateAuthor('test','testAuthor','','')
        author = Author.objects.filter(DISPLAY_NAME='test')[0]
        self.assertEqual(author.URL, '')

    def test_deleteAuthor(self):
        list_before = list(Author.objects.filter(DISPLAY_NAME='test'))
        deleteAuthor('test')
        list_after = list(Author.objects.filter(DISPLAY_NAME='test'))
        self.assertEqual(len(list_before) - len(list_after), 1)

    def test_addFriend(self):
        list_before = list(Author.objects.filter(DISPLAY_NAME='test')[0].FRIENDS.all())
        # print(list_before)
        addFriend('test', 'testfriend')
        list_after = list(Author.objects.filter(DISPLAY_NAME='test')[0].FRIENDS.all())
        # print("list_after",list_after)
        self.assertEqual(len(list_after) - len(list_before), 1)

    def test_getFriends(self):
        self.assertEqual(list(getFriends('test')), list(Author.objects.filter(DISPLAY_NAME='test')[0].FRIENDS.all()))

    def test_deleteFriend(self):
        addFriend('test', 'testfriend')
        list_before = list(Author.objects.filter(DISPLAY_NAME='test')[0].FRIENDS.all())
        deleteFriend('test', 'testfriend')
        list_after = list(Author.objects.filter(DISPLAY_NAME='test')[0].FRIENDS.all())
        self.assertEqual(len(list_before) - len(list_after), 1)

class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(ID=1)
        Author.objects.create(HOST='test', DISPLAY_NAME='test', URL='test', GITHUB='test')

    def test_createPost(self):
        list_before = list(Post.objects.filter(TITLE='test_title'))
        author = Author.objects.filter(DISPLAY_NAME='test')[0]
        timeline_before = list(author.TIMELINE.all())
        
        createPost('test_title','test','test','abc','text','content', author,'','')
        list_after = list(Post.objects.filter(TITLE='test_title'))
        author_after = Author.objects.filter(DISPLAY_NAME='test')[0]
        timeline_after = list(author_after.TIMELINE.all())
        self.assertEqual(len(list_after) - len(list_before), 1)
        self.assertEqual(len(timeline_after) - len(timeline_before), 1)
        

    def test_updatePost(self):
        
        self.assertEqual(updatePost(1, 'abc', '', '', '', '', '', '',''), True)


    def test_deletePost(self):
        self.assertEqual(deletePost(1), True)

class CommentTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(HOST='test', DISPLAY_NAME='test', URL='test', GITHUB='test')

    def test_createComment(self):
        # self.comment = createComment(self.author, 'comment test', 'text')
        self.assertEqual(createComment(self.author, 'comment test', 'text'), True)

    def test_updateComment(self):
        new_comment = Comment.objects.create(AUTHOR=self.author, COMMENT='update comment test', CONTENT_TYPE='text')
        self.assertEqual(updateComment(new_comment.ID), True)

    def test_deleteComment(self):
        new_comment = Comment.objects.create(AUTHOR=self.author, COMMENT='delete comment test', CONTENT_TYPE='text')
        self.assertEqual(deleteComment(new_comment.ID), True)