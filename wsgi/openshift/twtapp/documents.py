# This file contains the document definitions using the MongoEngine API.
# This is analogous to models.py when using the traditional Django ORM.

# Note: in this simple app, we create a simple auth system that stores
# passwords in plaintext. For anything close to practical, use the 
# MongoEngine authentication backend, that mimics (much of)
# the original Django `django.contrib.auth` functionality. RTFM for more.

from mongoengine import *


