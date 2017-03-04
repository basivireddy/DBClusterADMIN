from django.conf.urls import url
from . import views
app_name = 'mongodb'
urlpatterns = [

    url(r'^$', views.mongodbclusterlist, name='mongodbclusterlist'),
    url(r'^mongodbcluster/(?P<mongodbcluster_id>[0-9]+)/$', views.mongodbcluster_detail, name='mongodbcluster_detail'),

]

