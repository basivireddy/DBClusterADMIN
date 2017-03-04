from django.conf.urls import url
from . import views
app_name = 'couchdb'
urlpatterns = [

    url(r'^$', views.couchdbclusterlist, name='couchdbclusterlist'),
    url(r'^couchdbcluster/(?P<couchcluster_id>[0-9]+)/$', views.couchdbcluster_detail, name='couchdbcluster_detail'),
    url(r'^couchdbcluster/add/$', views.create_couchdbcluster, name='create_couchdbcluster'),
    url(r'^couchdbcluster/(?P<couchdbcluster_id>[0-9]+)/delete_couchdbcluster/$', views.delete_couchdbcluster, name='delete_couchdbcluster'),

]