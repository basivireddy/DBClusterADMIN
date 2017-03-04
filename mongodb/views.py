
from django.http import HttpResponse
from .models import MongodbCluster




from django.shortcuts import render, get_object_or_404


def mongodbclusterlist(request):
    clusterslist = MongodbCluster.objects.all()
    return render(request, 'mongodb/mongodbclusterlist.html', {'clusterslist': clusterslist})


def mongodbcluster_detail(request, mongodbcluster_id):
    cl = get_object_or_404(MongodbCluster, pk=mongodbcluster_id)
    clusterdeatils = cl.ips
    nodes = clusterdeatils.split(",")
    from pymongo import Connection
    c = Connection(nodes)
    cluster_detail = c.admin.command("replSetGetStatus")
    css = "col-md-" + str(12 / len(nodes))
    css_table = "table-responsive col-md-" + str(9 / (len(nodes)))
    nodes_details = []
    nodesnames = cl.names.split(",")
    for i in range(len(nodes)):
        nodes_details.append([nodesnames[i], nodes[i]])

    parameters = ['name', 'uptime', 'health', 'stateStr']
    cluster_deatils = {'name': [], 'uptime': [], 'health': [], 'stateStr': []}
    for i in cluster_detail['members']:
        for k in parameters:
            cluster_deatils[k].append(i[k])

    context = {
        'setname': cluster_detail['set'],
        'mongodbcluster': cl,
        'cluster_deatils': cluster_deatils,
        'css': css,
        'css_table': css_table,
        'nodes_details': nodes_details,
        'nodes': nodes,
    }

    return render(request, 'mongodb/mongodbcluster_detail.html', context)
