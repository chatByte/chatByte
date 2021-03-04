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
        # To do
        pass

    def getAuthorTest(self):
        self.assertEqual(getAuthor('test'),Author.objects.filter(DISPLAY_NAME=test)[0])

    def createAuthorTest(self):
        self.assertEqual(createAuthor('testHost','testAuthor','',''), True)

    def updateAuthorTest(self):
        self.assertEqual(updateAuthor('test'), True)
        # pass

    def deleteAuthorTest(self):
        self.assertEqual(deleteAuthor('test'), True)

class PostTestCase(TestCase):
    def setUp(self):
        self.assertEqual()

    def createPostTest(self):
        self.assertEqual()

    def updatePostTest(self):
        #TODO
        pass

    def deletePostTest(self):
        #TODO
        pass

class CommentTestCase(TestCase):
    def setUp(self):
        #TODO
        pass

    def createCommentTest(self):
        #TODO
        pass

    def updateCommentTest(self):
        #TODO
        pass

    def deleteCommentTest(self):
        #TODO
        pass

