from django.conf.urls.defaults import patterns, include, url

import twtapp.views

urlpatterns = patterns('twtapp.views',

    (r'^$', twtapp.views.home),
    (r'^login/next(?P<next_page>/.*)', 'login_view'),
    (r'^login/$', 'login_view'),
    (r'^logout/$', 'logout_view'),
    (r'^home/$', 'home'),
    (r'^post/$', 'post'),
    (r'^(?P<username>[^/]*)/$', 'user_page'),
    (r'^(?P<username>[^/]*)/statuses/(?P<tweet_id>[^/]*)/$', 'status'),
    (r'^follow/(?P<to_follow>[^/]*)/$', 'follow_view'),
    (r'^unfollow/(?P<the_creep>[^/]*)/$', 'unfollow_view'),
    
)

