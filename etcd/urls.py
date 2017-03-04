from django.conf.urls import url
from . import views
app_name = 'etcd'
urlpatterns = [

    url(r'^$', views.etcdclusterlist, name='etcdclusterlist'),
    url(r'^etcdcluster/(?P<etcdcluster_id>[0-9]+)/$', views.etcdcluster_detail, name='etcdcluster_detail'),
    url(r'^etcdcluster/add/$', views.create_etcdcluster, name='create_etcdcluster'),
    url(r'^etcdcluster/(?P<etcdcluster_id>[0-9]+)/delete_etcdcluster/$', views.delete_etcdcluster, name='delete_etcdcluster'),


]

