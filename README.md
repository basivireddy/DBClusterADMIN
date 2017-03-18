# Cluster ADMIN
It's a administration and monitoring tool for etcd,couchdb,mysql and mongodb clusters.

## ScreenShot: ##

![ScreenShot]()

-------

## Installation

### Create virtual environment and activate(optional)
```
    virtualenv ENV
    source ENV/bin/activate
```

### Download MusicBox
```
    git clone https://basivireddy@bitbucket.org/basivireddy/clustermonitoring.git
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

