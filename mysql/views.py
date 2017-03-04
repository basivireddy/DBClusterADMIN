from django.shortcuts import render
from django.http import HttpResponse
from .models import MysqlCluster
from django.shortcuts import render, get_object_or_404
from .forms import MysqlClusterForm
import json
import urllib2
# Create your views here.
def mysqlclusterlist(request):
    clusterslist = MysqlCluster.objects.all()
    return render(request, 'mysql/mysqlclusterlist.html', {'clusterslist': clusterslist})


def delete_mysqlcluster(request, mysqlcluster_id):
    cl = MysqlCluster.objects.get(pk=mysqlcluster_id)
    cl.delete()
    clusterslist = MysqlCluster.objects.all()
    return render(request, 'mysql/mysqlclusterlist.html', {'clusterslist': clusterslist})


def node_details(ip):
    details = {}
    import MySQLdb.cursors
    conn = MySQLdb.connect(host=ip,
                           port=3306,
                           user="root",
                           passwd="system123")

    cur = conn.cursor()
    cur.execute("SHOW  STATUS like 'wsrep_%'")
    data = cur.fetchall()
    cur.close()
    for t in data:
        details[t[0]] = t[1]
    return details


def slave_status(ip):
    details = {}
    try:
        import MySQLdb as mdb
        con = mdb.connect(host=ip,
                          port=3306,
                          user='root',
                          passwd='system123');

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute('show slave status')
        slave_status = cur.fetchone()
        slave_file = slave_status["Seconds_Behind_Master"]
        slave_sql_running = "1" if slave_status["Slave_SQL_Running"] == "Yes" else "0"
        slave_io_running = "1" if slave_status["Slave_IO_Running"] == "Yes" else "0"
        status = False
        if slave_sql_running == "1" and slave_io_running == "1":
            status = True

        details = {'Seconds_Behind_Master': str(slave_file), 'slave_io_running': slave_io_running,
                   'slave_sql_running': slave_sql_running, 'status': status, 's': True}
        return details
    except Exception, e:
        details = {'s': False, 'm': e}
        return details


def mysqlcluster_detail(request, mysqlcluster_id):
    mycl = get_object_or_404(MysqlCluster, pk=mysqlcluster_id)
    clusterdeatils = mycl.ips  # "172.17.0.2:5984,172.17.0.4:5984"
    nodes = clusterdeatils.split(",")
    cluster_deatilsall = {}
    for ip in nodes:
        cluster_deatilsall[ip] = node_details(ip)

    # cluster_deatils = {'172.14.2.13': {'wsrep_commit_oool': '0.000000', 'wsrep_local_send_queue_min': '0', 'wsrep_provider_name': 'Galera', 'wsrep_connected': 'ON', 'wsrep_cert_deps_distance': '9.970443', 'wsrep_commit_oooe': '0.000000', 'wsrep_desync_count': '0', 'wsrep_local_cached_downto': '1665226', 'wsrep_evs_evict_list': '', 'wsrep_cluster_conf_id': '11', 'wsrep_local_state': '4', 'wsrep_last_committed': '1665428', 'wsrep_evs_state': 'OPERATIONAL', 'wsrep_cert_index_size': '1', 'wsrep_local_recv_queue_min': '0', 'wsrep_received_bytes': '157787542', 'wsrep_repl_keys_bytes': '0', 'wsrep_flow_control_recv': '57', 'wsrep_protocol_version': '7', 'wsrep_local_state_comment': 'Synced', 'wsrep_apply_window': '1.000000', 'wsrep_provider_version': '25.3.17(r3619)', 'wsrep_local_send_queue_avg': '0.000000', 'wsrep_repl_data_bytes': '0', 'wsrep_local_recv_queue': '0', 'wsrep_cluster_status': 'Primary', 'wsrep_local_send_queue_max': '1', 'wsrep_cluster_size': '2', 'wsrep_local_replays': '0', 'wsrep_local_recv_queue_avg': '17.572917', 'wsrep_repl_keys': '0', 'wsrep_ready': 'ON', 'wsrep_replicated_bytes': '0', 'wsrep_evs_repl_latency': '0/0/0/0/0', 'wsrep_commit_window': '1.000000', 'wsrep_local_cert_failures': '0', 'wsrep_local_bf_aborts': '0', 'wsrep_received': '384', 'wsrep_local_send_queue': '0', 'wsrep_flow_control_paused': '0.000023', 'wsrep_local_commits': '0', 'wsrep_apply_oool': '0.000000', 'wsrep_repl_other_bytes': '0', 'wsrep_local_state_uuid': 'b5ad345b-983e-11e6-845e-1e277bfddb3f', 'wsrep_causal_reads': '0', 'wsrep_apply_oooe': '0.000000', 'wsrep_provider_vendor': 'Codership Oy <info@codership.com>', 'wsrep_cluster_state_uuid': 'b5ad345b-983e-11e6-845e-1e277bfddb3f', 'wsrep_flow_control_sent': '57', 'wsrep_evs_delayed': '', 'wsrep_replicated': '0', 'wsrep_local_index': '0', 'wsrep_gcomm_uuid': '8487b73d-9b7f-11e6-9c57-b372537ed467', 'wsrep_thread_count': '2', 'wsrep_flow_control_paused_ns': '18237831886', 'wsrep_local_recv_queue_max': '27', 'wsrep_cert_interval': '0.000000', 'wsrep_incoming_addresses': '172.14.2.13:3306,172.14.3.10:3306'}, '172.14.3.10': {'wsrep_commit_oool': '0.000000', 'wsrep_local_send_queue_min': '0', 'wsrep_provider_name': 'Galera', 'wsrep_connected': 'ON', 'wsrep_cert_deps_distance': '9.926471', 'wsrep_commit_oooe': '0.000000', 'wsrep_local_cached_downto': '1665225', 'wsrep_evs_evict_list': '', 'wsrep_cluster_conf_id': '11', 'wsrep_local_state': '4', 'wsrep_last_committed': '1665428', 'wsrep_evs_state': 'OPERATIONAL', 'wsrep_cert_index_size': '1', 'wsrep_local_recv_queue_min': '0', 'wsrep_received_bytes': '4460', 'wsrep_repl_keys_bytes': '3461418', 'wsrep_flow_control_recv': '57', 'wsrep_protocol_version': '7', 'wsrep_local_state_comment': 'Synced', 'wsrep_apply_window': '1.000000', 'wsrep_provider_version': '25.3.14(r3560)', 'wsrep_local_send_queue_avg': '0.061497', 'wsrep_repl_data_bytes': '154309538', 'wsrep_local_recv_queue': '0', 'wsrep_cluster_status': 'Primary', 'wsrep_local_send_queue_max': '2', 'wsrep_cluster_size': '2', 'wsrep_local_replays': '0', 'wsrep_local_recv_queue_avg': '0.021739', 'wsrep_repl_keys': '432028', 'wsrep_ready': 'ON', 'wsrep_replicated_bytes': '157784012', 'wsrep_evs_repl_latency': '0/0/0/0/0', 'wsrep_commit_window': '1.000000', 'wsrep_local_cert_failures': '0', 'wsrep_local_bf_aborts': '0', 'wsrep_received': '184', 'wsrep_local_send_queue': '0', 'wsrep_flow_control_paused': '0.000024', 'wsrep_local_commits': '172', 'wsrep_apply_oool': '0.000000', 'wsrep_repl_other_bytes': '0', 'wsrep_local_state_uuid': 'b5ad345b-983e-11e6-845e-1e277bfddb3f', 'wsrep_causal_reads': '0', 'wsrep_apply_oooe': '0.000000', 'wsrep_provider_vendor': 'Codership Oy <info@codership.com>', 'wsrep_cluster_state_uuid': 'b5ad345b-983e-11e6-845e-1e277bfddb3f', 'wsrep_flow_control_sent': '0', 'wsrep_evs_delayed': '', 'wsrep_replicated': '204', 'wsrep_local_index': '1', 'wsrep_gcomm_uuid': '9c4a344f-078c-11e6-966a-ef39693d882c', 'wsrep_thread_count': '2', 'wsrep_flow_control_paused_ns': '19123261691', 'wsrep_local_recv_queue_max': '2', 'wsrep_cert_interval': '0.000000', 'wsrep_incoming_addresses': '172.14.2.13:3306,172.14.3.10:3306'}}
    cluster_deatils = {'wsrep_cluster_size': [], 'wsrep_cluster_status': [], 'wsrep_connected': [], 'wsrep_ready': [],
                       'wsrep_incoming_addresses': [], 'wsrep_evs_delayed': [], 'wsrep_evs_evict_list': [],
                       'wsrep_evs_repl_latency': [], 'wsrep_evs_state': [], 'wsrep_local_recv_queue_avg': []}
    parameters = ['wsrep_cluster_size', 'wsrep_cluster_status', 'wsrep_connected', 'wsrep_ready',
                  'wsrep_incoming_addresses', 'wsrep_evs_delayed', 'wsrep_evs_evict_list', 'wsrep_evs_repl_latency',
                  'wsrep_evs_state', 'wsrep_local_recv_queue_avg']

    for cluserip in cluster_deatilsall.keys():
        for parameter in cluster_deatils.keys():
            if cluster_deatilsall[cluserip][parameter]:
                value = cluster_deatilsall[cluserip][parameter]
            else:
                value = "NA"

            cluster_deatils[parameter].append(value)

    cluster_data = {'nodes': []}

    nodes_details = []
    nodesnames = mycl.names.split(",")
    for i in range(len(nodes)):
        nodes_details.append([nodesnames[i], nodes[i]])

    slave_details = {}
    if mycl.numofsalvenodes >= 1:
        slaveips = mycl.slaveips.split(",")
        slavenames = mycl.slavenames.split(",")
        slave_data = {}
        for i in range(mycl.numofsalvenodes):
            slave = slave_status(slaveips[i])
            if slave['s']:
                slave_details[slavenames[i]] = {'ip': slaveips[i]}
                slave_details[slavenames[i]].update(slave)
            else:
                slave_details = slave
    else:
        slave_details = {}

    print slave_details
    css = "col-md-" + str(12 / len(nodes))
    css_table = "table-responsive col-md-" + str(9 / (len(nodes)))

    context = {
        'mysqlcluster': mycl,
        'nodes': nodes,
        'cluster_deatils': cluster_deatils,
        'css': css,
        'css_table': css_table,
        'parameters': parameters,
        'cluster_data': cluster_data,
        'slave_details': slave_details,
        'nodes_details': nodes_details,

    }

    return render(request, 'mysql/mysqlcluster_detail.html', context)


def create_mysqlcluster(request):
    form = MysqlClusterForm(request.POST or None)
    if form.is_valid():
        mysqlcluster = form.save(commit=False)
        mysqlcluster.save()
        return render(request, 'mysql/mysqlcluster_detail.html', {'mysqlcluster': mysqlcluster})
    context = {
        "form": form,
    }
    return render(request, 'mysql/create_mysqlcluster.html', context)
