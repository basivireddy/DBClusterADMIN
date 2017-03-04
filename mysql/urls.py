from django.conf.urls import url
from . import views
app_name = 'mysql'
urlpatterns = [

    url(r'^$', views.mysqlclusterlist, name='mysqlclusterlist'),
    url(r'^mysqlcluster/(?P<mysqlcluster_id>[0-9]+)/$', views.mysqlcluster_detail, name='mysqlcluster_detail'),
    url(r'^mysqlcluster/add/$', views.create_mysqlcluster, name='create_mysqlcluster'),
    url(r'^mysqlcluster/(?P<mysqlcluster_id>[0-9]+)/delete_mysqlcluster/$', views.delete_mysqlcluster,name='delete_mysqlcluster'),

]