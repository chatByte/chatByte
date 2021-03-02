from django.test import TestCase
from .models import Author, Post, Comment

# Create your tests here.

class AuthorApiCase(TestCase):
    def setUp(self):
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

class PostApiCase(TestCase):
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

class CommentApiCase(TestCase):
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