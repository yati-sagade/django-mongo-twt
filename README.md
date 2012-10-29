Django-Mongo-Twt on OpenShift Express
=====================================

This is a simple twitter clone along the lines of 
https://github.com/openshift/openshift-twt-mongo-demo

This project is intended to serve as a reasonable example for people who'd like
to use Django + MongoDB on Express with MongoEngine.

The aim is to use MongoDB with Mongoengine, a convenient wrapper library over 
PyMongo that emulates most of the common Django functionality, including auth.
The result is a familiar API for database access so that the switch to NoSQL
MongoDB can be relatively painless for Django users.

Please drop me a line if you find any bugs/glitches at yati dot sagade at gmail dot com or better still,
fork, hack and send a pull request ;)


Quickstart

1) Create an account at http://openshift.redhat.com/

2) Create a python application and attach mongodb to it:
    
    rhc app create -a twt -t python-2.6
    rhc app cartridge add -a twt -c mongodb-2.0

3) Add this upstream repo
    
    cd twt
    git remote add upstream -m master git://github.com/yati-sagade/django-mongo-twt.git
    git pull -s recursive -X theirs upstream master

4) Then push the repo upstream

    git push

5) That's it, you can now browse to your application at:

http://twt-$yournamespace.rhcloud.com

