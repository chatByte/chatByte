from .models import Author
from .models import Post
from .models import Comment

def createAuthor(host, display_name, url, github):
    Author.objects.create(HOST=host, DISPLAY_NAME=display_name, URL=url, GITHUB=github)

def updateAuthor(id):
    #TODO
    author = Author.objects.filter(ID=id)
    # update element here
    author.save()
    pass

def deleteAuthor():
    #TODO
    pass

def createPost(title, source, origin, description, content_type, content, author, categories, visibility):
    #TODO keep track of COMMENTS_NO and PAGE_SIZE, COMMENTS_FIRST_PAGE
    Post.objects.create(TITLE=title, SOURCE=source, ORIGIN=origin, DESCIPTION=description, CONTENT_TYPE=content_type, CONTENT=content\
        , AUTHOR=author, CATEGORIES=categories, COMMENTS_NO=0, PAGE_SIZE=0, COMMENTS_FIRST_PAGE='', VISIBILITY=visibility)

def updatePost(id):
    post = Post.objects.filter(ID=id)
    # update field here
    post.save()

def deletePost():
    #TODO
    pass

def createComment():
    #TODO
    pass

def updateComment(id):
    #TODO
    comment = Comment.objects.filter(ID=id)
    # update field here
    comment.save()
    pass

def deleteComment():
    #TODO
    pass