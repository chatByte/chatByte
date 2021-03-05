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
        # pass
        
    def test_validActor(self):
        self.assertEqual(validActor('test123', '123'), False)
        self.assertEqual(validActor('test', '123'), True)

class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.create(HOST='test', DISPLAY_NAME='test', URL='test', GITHUB='test')
        Author.objects.create(HOST='testfriend', DISPLAY_NAME='testfriend', URL='testfriend', GITHUB='testfriend')
        
    def test_addFriend(self):
        self.assertEqual(addFriend('test', 'testFriend'), True)

    def test_getTimeline(self):
        self.assertEqual(getTimeline('test'), Author.objects.filter('test').TIMELINE)

    def test_getAuthor(self):
        self.assertEqual(getAuthor('test'), Author.objects.filter(DISPLAY_NAME=test)[0])

    def test_createAuthor(self):
        self.assertEqual(createAuthor('testHost','testAuthor','',''), True)

    def test_updateAuthor(self):
        self.assertEqual(updateAuthor('test'), True)
        # pass

    def test_deleteAuthor(self):
        self.assertEqual(deleteAuthor('test'), True)

class PostTestCase(TestCase):
    # title, source, origin, description, content_type, content, author, categories, visibility
    def setUp(self):
        # Author.objects.create(USERNAME='test', PASSWORD='123')
        pass

    def createPostTest(self):
        self.assertEqual(createPost('test_title','test','test','abc','text','content','test','',''), True)

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

