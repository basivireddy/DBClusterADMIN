from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from .models import EtcdCluster
from .forms import EtcdClusterForm
import json
import urllib2
def etcdclusterlist(request):
    clusterslist = EtcdCluster.objects.all()
    return render(request, 'etcd/etcdclusterlist.html', {'clusterslist':clusterslist })


def delete_etcdcluster(request, etcdcluster_id):
        cl = EtcdCluster.objects.get(pk=etcdcluster_id)
        cl.delete()
        clusterslist = EtcdCluster.objects.all()
        return render(request, 'etcd/etcdclusterlist.html', {'clusterslist': clusterslist})

def runlocal(cmd):
    #import subprocess
    #return subprocess.check_call([cmd])
    from subprocess import Popen, PIPE
    #cmd = "ls -l ~/"
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()

    return {"status": p.returncode , "output": out.rstrip() ,"error":err.rstrip()}

def startnode(sip,ip,member,etcdcl,cmd):
    # start node
    name = ""
    ips = etcdcl.ips.split(",")
    names = etcdcl.nodesname.split(",")
    other_nodes = []
    for item in range(len(ips)):
        if ips[item] == ip:
            name = names[item]
        else:
            other_nodes.append([ips[item], names[item]])


    other_nodes_peerurls = ""
    for other_nodes in other_nodes:
        other_nodes_peerurls += "," + other_nodes[1] + "=http://" + other_nodes[0] + ":" + etcdcl.peerport

    if cmd == "all":
        insrtuctions = "rm -rf  /root/" + name + ".etcd/" + "\n" + "etcdctl -C " \
                   + sip + ":" + etcdcl.clientport + " member remove  " + member + \
                   "\n" + "etcdctl -C " + sip + ":" + etcdcl.clientport + " member add " + \
                   name + "  http://" + ip + ":" + etcdcl.peerport + "\n" + "nohup etcd -snapshot-count=0 -proxy-refresh-interval 20000 -name " + \
                   name + " -initial-advertise-peer-urls  http://" + ip + ":" + etcdcl.peerport + \
                   " -listen-peer-urls  http://" + ip + ":" + etcdcl.peerport + " -listen-client-urls http://" + \
                   ip + ":" + etcdcl.clientport + ",http://127.0.0.1:" + etcdcl.clientport + " -advertise-client-urls http://" + \
                   ip + ":" + etcdcl.clientport + " -initial-cluster-token clientdht -initial-cluster " + \
                   name + "=http://" + ip + ":" + etcdcl.peerport + other_nodes_peerurls + " -initial-cluster-state existing &"
    else:
        insrtuctions = "nohup etcd -snapshot-count=0 -proxy-refresh-interval 20000 -name " + \
                       name + " -initial-advertise-peer-urls  http://" + ip + ":" + etcdcl.peerport + \
                       " -listen-peer-urls  http://" + ip + ":" + etcdcl.peerport + " -listen-client-urls http://" + \
                       ip + ":" + etcdcl.clientport + ",http://127.0.0.1:" + etcdcl.clientport + " -advertise-client-urls http://" + \
                       ip + ":" + etcdcl.clientport + " -initial-cluster-token clientdht -initial-cluster " + \
                       name + "=http://" + ip + ":" + etcdcl.peerport + other_nodes_peerurls + " -initial-cluster-state existing &"

    return insrtuctions

def ectdnewcluster(etcdcl):
    ips = etcdcl.ips.split(",")
    names = etcdcl.nodesname.split(",")
    peerport = etcdcl.peerport
    clientport = etcdcl.clientport
    cluster_deatils = []

    nodes_peerurls = ""
    clen = len(ips)
    for i in range(clen -1 ):
        nodes_peerurls += names[i]+"=http://"+ips[i]+":"+peerport+","

    nodes_peerurls += names[clen -1 ]+"=http://"+ips[clen -1]+":"+peerport


    for i in range(len(ips)):
        insrtuctions = "rm -rf /root/" + names[i] + ".etcd/" + "\n"  \
                       + "nohup etcd -name " +names[i] + " -initial-advertise-peer-urls http://"+ips[i]+":"+peerport + " -listen-peer-urls http://" \
                       + ips[i]+":"+peerport + " -listen-client-urls http://"+ips[i]+":"+clientport+ ",http://127.0.0.1:"+clientport \
                       + " -advertise-client-urls http://"+ips[i]+":"+clientport +" -initial-cluster-token "+etcdcl.cname+" -initial-cluster " + nodes_peerurls \
                       + " -initial-cluster-state new &"

        cluster_deatils.append([ips[i],"Deploying Etcd Cluster",1,insrtuctions])

    return  cluster_deatils




import re
def etcdcluster_detail(request, etcdcluster_id):
    etcdcl = get_object_or_404(EtcdCluster, pk=etcdcluster_id)
    ips = etcdcl.ips.split(",")
    names = etcdcl.nodesname.split(",")
    cluster_deatils = []
    startnode_d = {"ip":[]}
    isdeployed = etcdcl.isdeployed
    ip_member={}

    if not isdeployed :
        cluster_deatils = ectdnewcluster(etcdcl)
    else:
      isclustercollapsed = len(ips)
      insrtuctions = ""
      for ip in ips:
        cmd = "etcdctl -C "+ip+":"+etcdcl.clientport+" cluster-health"
        clusterhealth = runlocal(cmd)
        print clusterhealth
        #health_sc = len(ips)

        if clusterhealth['status'] == 0 or clusterhealth['status'] == 5:
           health = clusterhealth['output']

           health_s = 0
           #health_sc = len(ips)
           health = health.splitlines()
           c_statusmessage = health[-1]
           for line in health:
               if not re.search(r'^member',line):
                   health.remove(line)
           health_deatils = []
           for i in health:
               data = i.split(" ")
               member = data[1]
               status = 1
               if re.search(r'http://', i):
                   #if not member in ip_member:
                     ip_member[str(i.split("http://")[1].split(":")[0])] = member
               if data[3] == "healthy:":
                   status = 0

               message = i
               health_deatils.append([member, status, message])

        else:
           health_deatils = ["unable to connect node"]
           health_s = 1
           health_sc = 0
           startnode_d['ip'].append(ip)
           isclustercollapsed -= 1
           c_statusmessage = "unable to connect node"



        cluster_deatils.append([ip,health_deatils,health_s,insrtuctions,c_statusmessage])

      if isclustercollapsed == 0:
          cluster_deatils = ectdnewcluster(etcdcl)
      else:
       sips = list(set(ips) - set(startnode_d["ip"]))
       #for ip in startnode_d['ip']:
       print startnode_d['ip']
       print ip_member
       if len(startnode_d['ip']) == len(ip_member.keys()) - 1  and  set(startnode_d['ip']) < set(ip_member.keys()) :
           cmd = "etcd only"
       else:
           cmd = "all"
       for node in cluster_deatils:
            if node[0] in startnode_d['ip'] and node[0] in ip_member:
               sip = sips[0]
               print type(str(ip)),
               ip = node[0]
               node[3] = startnode(sip,ip,ip_member[ip],etcdcl,cmd)

            elif node[0] in startnode_d['ip'] and not node[0] in ip_member:
                for item in range(len(ips)):
                    if ips[item] == node[0]:
                        name = names[item]
                node[3] =  "etcdctl -C " + sips[0] + ":" + etcdcl.clientport + " member add " + name + "  http://" + node[0] + ":" + etcdcl.peerport
                node[3] = startnode(sips[0], node[0] , "", etcdcl,cmd)


    context = {

        'ips': ips,
        'etcdcluster':etcdcl,
        'cluster_deatils':cluster_deatils,
        'ip_member':ip_member,
    }

    return render(request, 'etcd/etcdcluster_detail.html', context)






def create_etcdcluster(request):
        form = EtcdClusterForm(request.POST or None)
        if form.is_valid():
            etcdcluster = form.save(commit=False)
            etcdcluster.save()
            return render(request, 'etcd/etcdcluster_detail.html', {'etcdcluster': etcdcluster})
        context = {
            "form": form,
        }
        return render(request, 'etcd/create_etcdcluster.html', context)

# Create your views here.
