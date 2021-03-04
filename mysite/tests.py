from django.test import TestCase
 
from chat.models import Author, Post, Comment, Actor
from chat.api import validActor
# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        #TODO
        Actor.objects.create(ID='1', USERNAME='test', PASSWORD='123')
        pass

    def test_validActor(self):
        self.assertEqual(validActor('test', '123'), True)

class AuthorTestCase(TestCase):
    def setUp(self):
        #TODO
        # Animal.objects.create(name="lion", sound="roar")
        # Animal.objects.create(name="cat", sound="meow")
        pass

    def addFriendTest(self):
        #TODO
        pass

    def getTimelineTest(self):
        #TODO
        pass

    def getAuthorTest(self):
        #TODO
        pass

    def createAuthorTest(self):
        #TODO
        pass

    def updateAuthorTest(self):
        #TODO
        pass

    def deleteAuthorTest(self):
        #TODO
        pass

class PostTestCase(TestCase):
    def setUp(self):
        #TODO
        pass

    def createPostTest(self):
        #TODO
        pass

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