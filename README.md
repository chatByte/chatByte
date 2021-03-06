# chatByte
Project wiki: https://github.com/chatByte/chatByte/wiki 

Working progress controled by our product backlog: https://github.com/chatByte/chatByte/projects/1

## Required installation:
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
https://project-chatbyte.herokuapp.com/chat/login/

## Local host:
inside chatByte/mysite
python3 manage.py runserver

## Some additional command guide:
inside chatByte/mysite

run:
	python manage.py runserver, or python3 manage,oy runserver depends on venv

test:
	python manage.py test

user:
	python manage.py createsuperuser
