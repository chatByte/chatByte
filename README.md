# chatByte
Project wiki: https://github.com/chatByte/chatByte/wiki 

We are happy to answer your questions; you can always reach out to us by the contact information listed in our wiki.

Working progress controled by our product backlog: https://github.com/chatByte/chatByte/projects/1


## API documentation:
:bowtie: FULL API doc <br />
https://github.com/chatByte/chatByte/blob/main/API_docs.md <br />
:bowtie: API endpoint URL doc <br />
https://github.com/chatByte/chatByte/blob/main/API_publicEndPoints.md<br />
## Required installation:
- Django
- Djongo
- mongodb

Please refer to the resources for more instruction at: https://github.com/chatByte/chatByte/wiki/Resources

## Start running the app
First git clone the repo:

    git clone https://github.com/chatByte/chatByte.git
Then, create a virtual environmen:

    cd chatByte
    virtualenv venv
    source venv/bin/activate

Finally, go to the outer mysite directory and run the app using the makefile command:

    cd mysite
    make run

To run the test cases, make sure you are in the outer mysite directory:

    make test

## Herokuapp login method:
https://app-chatbyte.herokuapp.com/

https://chatbyte.herokuapp.com/

## Connected distribute server:
### (fully connected, two way connection)
* Group 5 
https://github.com/CMPUT404-wi21-project/CMPUT404-project-socialdistribution
* Our Two herokuapps
### (basic connection, two way connection)
* Group 14 
https://github.com/CMPUT404ProjectTeam2021W/Jan28-group-cmput404-project



## Local host:
inside chatByte/mysite
python3 manage.py runserver

## Some additional command guide:
In the chatByte/mysite directory:

#### command to start the server:

    python manage.py runserver, or python3 manage,oy runserver depends on venv

#### command to run the test:

    python manage.py test

#### command to create an admin:

    python manage.py createsuperuser
    
## Restful endpoints  :smirk:

    This a full Restful application,  For more details you can always look up our documentaion, and have fun; 
    
   
    chat/author/<author_id>/                                   (profile html / single author endpoint)
    chat/author/<author_id>/posts                              (home html / list of posts endpoint)
    chat/author/<author_id>/posts/<post_id>                    (profile html / single post endpoint)
    chat/author/<author_id>/friends                            (friends html / list of authors endpoint)
    chat/author/<author_id>/friends/<author_id>                (friendProfile html / list of authors endpoint)
    chat/author/<author_id>/posts/<post_id>/comments           (profile html / list of comments endpoint)
