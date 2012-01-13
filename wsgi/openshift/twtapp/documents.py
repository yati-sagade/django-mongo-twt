# This file contains the document definitions using the MongoEngine API.
# This is analogous to models.py when using the traditional Django ORM.

# Note: in this simple app, we create a simple auth system that stores
# passwords in plaintext. For anything close to practical, use the 
# MongoEngine authentication backend, that mimics (much of)
# the original Django `django.contrib.auth` functionality. RTFM for more.

from mongoengine import *
from mongoengine.django.auth import User
import uuid

class Post(Document):
    '''Encapsulate a user post.
    We generate the _id field ourselves, as in the original example.
    '''
    uid = StringField()
    _id = StringField(default=uuid.uuid4().hex)
    content = StringField()

    def __unicode__(self):
        return '{0}: {1}'.format(self.uid, self.content[:30])

    def getId(self):
        '''This is necessary, as Django's template system does not allow us to
        say tweet._id, but allows tweet.getId (Template variable/atrribute names 
        may not begin with underscores.'''
        return self._id

    @classmethod
    def get_post_by_id(kls, pid):
        return kls.objects.get(_id=pid)
#-------------------------------------------------------------------------------
class UserProfile(User):
    '''Encapsulates a user profile. We subclass the mongoengine User class for
    simplicity. We then add the fields required for followers, following, posts
    and timeline.
    '''
    follower = ListField(StringField())
    followee = ListField(StringField())
    timeline = ListField(StringField())
    posts = ListField(StringField())

    def __unicode__(self):
        return User.__unicode__(self)

    def get_followers(self):
        return (self.__class__.objects.get(username=f_id) for f_id in self.follower)

    def get_following(self):
        return (self.__class__.objects.get(username=f_id) for f_id in self.followee)

    def get_posts(self):
        return (Post.objects.get(_id=p_id) for p_id in self.posts)

    def get_timeline(self):
        return (Post.objects.get(_id=p_id) for p_id in self.timeline)

    def add_post(self, content):
        post = Post(content=content, uid=self.username)
        post.save()
        self.posts.append(post._id)
        self.save()

        return post

    def add_to_timeline(self, post):
        '''takes a Post and adds it to the user's timeline'''
        self.timeline.append(post._id)
        self.save()
        return post
   
    @classmethod
    def get_user_by_id(kls, uid):
        return kls.objects.get(username=uid)

    @classmethod
    def find(kls, uid):
        try:
            user = kls.get_user_by_id(uid)
        except kls.DoesNotExist:
            return None

        return user
#-------------------------------------------------------------------------------
