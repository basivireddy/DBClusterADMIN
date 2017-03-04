from django.shortcuts import render
from django.http import HttpResponse
from .models import CouchCluster
from .forms import CouchClusterForm
import json
import urllib2
from django.shortcuts import render, get_object_or_404

def comparedbs(ip1, ip2, jd1, jd2):
    s = {}
    dict1 = {}
    dict2 = {}
    dictr1 = {}
    dictr2 = {}
    s['docs'] = {}
    if jd1 != jd2:
        s['status'] = 1
        s['message'] = "both nodes have different databases"
        union = jd1 + jd2
        r1 = list(set(union) - set(jd1))
        r2 = list(set(union) - set(jd2))
        s['commondbs'] = list((set(union) - set(r1)) - set(r2))
        # print r1,r2
        l_r1 = len(r1)
        l_r2 = len(r2)
        if l_r1 < l_r2:
            s['maxl'] = range(l_r2)
        elif l_r1 > l_r2:
            s['maxl'] = range(l_r1)
        if l_r1 != 0:
            s['a1'] = r1
            for i in r1:
                dictr2[i] = json.loads(urllib2.urlopen("http://" + ip2 + "/" + i + "/").read().strip(' \t\n\r'))[
                    'doc_count']
            s['docs']['rd2'] = dictr2

        if l_r2 != 0:
            s['a2'] = r2
            for i in r2:
                dictr1[i] = json.loads(urllib2.urlopen("http://" + ip1 + "/" + i + "/").read().strip(' \t\n\r'))[
                    'doc_count']
            s['docs']['rd1'] = dictr1
    else:
        s['status'] = 0
        s['message'] = "both nodes have same databases"
        s['commondbs'] = jd1

    docstatus = True
    for i in s['commondbs']:
        a = json.loads(urllib2.urlopen("http://" + ip1 + "/" + i + "/").read().strip(' \t\n\r'))['doc_count']
        b = json.loads(urllib2.urlopen("http://" + ip2 + "/" + i + "/").read().strip(' \t\n\r'))['doc_count']

        if a == b:
            dict1[i] = [a, b, True]
        else:
            docstatus = False
            dict1[i] = [a, b, False]

    if docstatus:
        s['docstatus'] = 0
        s['docmessage'] = "both nodes have same number of docs"
    else:
        s['docstatus'] = 1
        s['docmessage'] = "both nodes have different number of docs"

    s['docs']['cd1'] = dict1
    # s['docs']['cd2'] = dict2

    return s


def couchdbclusterlist(request):
    clusterslist = CouchCluster.objects.all()
    return render(request, 'couchdb/couchclusterlist.html', {'clusterslist': clusterslist})


def delete_couchdbcluster(request, couchcluster_id):
    cl = CouchCluster.objects.get(pk=couchcluster_id)
    cl.delete()
    clusterslist = CouchCluster.objects.all()
    return render(request, 'couchdb/couchclusterlist.html', {'clusterslist': clusterslist})


def couchdbcluster_detail(request, couchcluster_id):
    cl = get_object_or_404(CouchCluster, pk=couchcluster_id)
    clusterdeatils = cl.ips  # "172.17.0.2:5984,172.17.0.4:5984"
    nodes = clusterdeatils.split(",")
    ip1 = nodes[0]
    ip2 = nodes[1]
    # print nodes, type(ip1)
    cl1 = "http://" + ip1 + "/_all_dbs"
    cl2 = "http://" + ip2 + "/_all_dbs"

    # r1 =

    d1 = urllib2.urlopen(cl1).read().strip(' \t\n\r')
    d2 = urllib2.urlopen(cl2).read().strip(' \t\n\r')
    jd1 = json.loads(d1)[2:]
    jd2 = json.loads(d2)[2:]

    context = {
        'couchcluster': cl,
        'ip1': ip1,
        'ip2': ip2,
        'comdbs': comparedbs(ip1, ip2, jd1, jd2)
        # 'comdbs':{'status': 0, 'commondbs': [u'users'], 'docs': {'cd1': {u'users': 348}, 'cd2': {u'users': 348}}, 'message': 'both nodes have same databases', 'docmessage': 'both nodes have same number of docs', 'docstatus': 0},
    }

    return render(request, 'couchdb/couchcluster_detail.html', context)


def create_couchdbcluster(request):
    form = CouchClusterForm(request.POST or None)
    if form.is_valid():
        couchcluster = form.save(commit=False)
        couchcluster.save()
        return render(request, 'couchdb/couchcluster_detail.html', {'couchcluster': couchcluster})
    context = {
        "form": form,
    }
    return render(request, 'couchdb/create_couchcluster.html', context)
