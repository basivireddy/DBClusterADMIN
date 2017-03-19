# Cluster ADMIN
An Administration and Monitoring tool for Etcd, CouchDB, MySQL and MongoDB clusters.

[**Installation Instructions**](#installation) 

------

## ScreenShot: ##
Etcd
![ScreenShot](ScreenShots/etcdcluster.png)
When One of Node down
![ScreenShot](ScreenShots/etcdclusteronenodedown.png)
CouchDB
![ScreenShot](ScreenShots/couchdbcluster1.png)
When Cluster have different databases
![ScreenShot](ScreenShots/couchdbcluster2.png)
When Cluster have different databases and different doc's in databases
![ScreenShot](ScreenShots/couchdbcluster3.png)
MongoDB
![ScreenShot](ScreenShots/mongodbcluster.png)
MySQL
![ScreenShot](ScreenShots/mysqlcluster.png)
-------

## Installation

### Create virtual environment and activate(optional)
```
    virtualenv ENV
    source ENV/bin/activate
```

### Download ClusterADMIN
```
    git clone https://github.com/basivireddy/ClusterADMIN.git
```

### Install  required packages
```
   apt-get install python-pip
   apt-get install python-dev libmysqlclient-dev
   cd clustermonitoring
   pip install -r requirements.txt
```
### Run the server
```
   python manage.py runserver 0.0.0.0:8000
```
then browse ***http://your_server_ip:8000/etcd/***

