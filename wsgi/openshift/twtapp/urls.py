from django.conf.urls.defaults import url, patterns
import views

urlpatterns = patterns(
               url(r'^$', views.home), 
        )
