from django.test import TestCase
from chat.models import Author, Post, Comment
from chat.api import validUser
# Create your tests here.

class UserTestCase(TestCase):
    
    def setUp(self):
        # set up 
        User.objects.create(USERNAME='test', PASSWORD='123')
        User.objects.create(USERNAME='testfriend', PASSWORD='123')
        # User.objects.create(USERNAME='testfriend', PASSWORD='123')
        # pass
        
    def test_validUser(self):
        
        self.assertEqual(validUser('test123', '123'), False)
        self.assertEqual(validUser('test', '123'), True)

    def test_addFriend(self):
        self.assertEqual(addFriend('test', 'testFriend'), True)
        
    
    def test_getAuthor(self):
        self.assertEqual(getAuthor(), A)

class AuthorTestCase(TestCase):
    def setUp(self):
        User.objects.create(USERNAME='test', PASSWORD='123')
        User.objects.create(USERNAME='testfriend', PASSWORD='123')
        
    def addFriendTest(self):
        self.assertEqual(addFriend('test', 'testFriend'), True)

    def getTimelineTest(self):
        self.assertEqual(getTimeline('test'), Author.objects.filter('test').TIMELINE)

    def getAuthorTest(self):
        self.assertEqual(getAuthor('test'),Author.objects.filter(DISPLAY_NAME=test)[0])

    def createAuthorTest(self):
        self.assertEqual(createAuthor('testHost','testAuthor','',''), True)

    def updateAuthorTest(self):
        self.assertEqual(updateAuthor('test'), True)

    def deleteAuthorTest(self):
        self.assertEqual(deleteAuthor('test'), True)

class PostTestCase(TestCase):
    title, source, origin, description, content_type, content, author, categories, visibility
    def setUp(self):
        Post.objects.create(ID=1)

    def createPostTest(self):
        self.assertEqual(createPost)

    def updatePostTest(self):
        self.assertEqual(updatePost(1), True)

    def deletePostTest(self):
        self.assertEqual(deletePost(1), True)

class CommentTestCase(TestCase):
    def setUp(self):
        author = Author.objects.create(HOST='test', DISPLAY_NAME='test', URL='test', GITHUB='test')

    def createCommentTest(self):
        self.assertEqual(createPost(author, '', 'text'), True)

    def updateCommentTest(self):
        self.assertEqual(updateComment(1), True)

    def deleteCommentTest(self):
        self.assertEqual(deleteComment(1), True)

