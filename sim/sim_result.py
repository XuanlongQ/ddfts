from models import *
from tool import performance
LEVEL = 'DEBUG'

@performance(LEVEL)
def packet_tracer(input_file_name):

    input_file = open(input_file_name, 'r')
    stime_dict = {} #start time for each flow
    etime_dict = {} #end time
    thrput_dict = {} #flow throughput
    pktcnt_dict = {} #packet count for each flow
    drcnt_dict = {} #droped packet count for each flow
    src_dict = {}
    dst_dict = {}
    for line in input_file:
        #print len(line.strip().split(' '))
        action, time, frm, to, tp, pktsize, flag, flow_id, src, dst, seq_no, packet_id = line.strip().split(' ')
        time = float(time)
        pktsize = int(pktsize)

        if not flow_id in stime_dict:
            stime_dict[flow_id] = float(time)
            etime_dict[flow_id] = float(time)
            src_dict[flow_id] = src.split('.')[0]
            dst_dict[flow_id] = dst.split('.')[0]
        if not flow_id in thrput_dict:
            thrput_dict[flow_id] = 0
        if not flow_id in drcnt_dict:
            drcnt_dict[flow_id] = 0
            pktcnt_dict[flow_id] = 0

        dst_node, dst_port = dst.split('.')
        src_node, src_port = src.split('.')
        #node 'to' receive and 'to' is dst_node and dst_node is flow[flow_id]'s dst
        if action == 'r' and to == dst_node and dst_dict[flow_id] == dst_node:
            etime_dict[flow_id] = time
            thrput_dict[flow_id] += pktsize
            pktcnt_dict[flow_id] += 1
        #node 'to' receive and 'to' is dst_node and dst_node is flow[flow_id]'s src
        elif action == 'r' and to == dst_node and src_dict[flow_id] == dst_node:
            thrput_dict[flow_id] += pktsize
            pktcnt_dict[flow_id] += 1
        elif action == 'd':
            drcnt_dict[flow_id] += 1
        elif action == 'r':
          #print 'to =%s, src_node=%s, src_dict[flow_id]=%s' % (to, src_node, src_dict[flow_id])
          pass

    input_file.close()

    id_list = sorted(stime_dict.keys(), lambda x,y: cmp(int(x),int(y)))
    if False:
            for flow_id in id_list:
                start = stime_dict[flow_id]
                end = etime_dict[flow_id]
                duration = end - start
                fsize = thrput_dict[flow_id]
                pktcnt = pktcnt_dict[flow_id]
                drcnt = drcnt_dict[flow_id]
                line = '%s %f %d %d %d\n' % (flow_id, duration, fsize, pktcnt, drcnt)
                if start < end:
                    #print 'flow %s: duration = %f, fsize=%d, drcnt = %d' % (flow_id, duration, fsize, drcnt)
                    #print line,
                    pass

    return (id_list, stime_dict, etime_dict, drcnt_dict, thrput_dict, pktcnt_dict)

@performance(LEVEL)
def flow_tracer(input_file_name):
    qfc, sfc, lfc, afc = (0, 0, 0, 0)
    ftype_dict = {}
    deadline_dict = {}
    src_dict = {}
    dst_dict = {}
    size_dict = {}

    input_file = open(input_file_name, 'r')
    for line in input_file:
        if line.startswith('qfc'):
            qfc = int(line.strip().split(':')[1])

        elif line.startswith('sfc'):
            sfc = int(line.strip().split(':')[1])
            
        elif line.startswith('lfc'):
            lfc = int(line.strip().split(':')[1])
            
        elif line.startswith('afc'):
            afc = int(line.strip().split(':')[1])
            
        elif line.startswith('flow:'):
            finfo = line.strip().split('|')
            #print 'finfo:'
            #print finfo
            fid = finfo[0].split(':')[1]
            ftype_dict[fid] = finfo[1].split(':')[1]
            deadline_dict[fid] = finfo[2].split(':')[1]
            src_dict[fid] = finfo[3].split(':')[1]
            dst_dict[fid] = finfo[4].split(':')[1]
            size_dict[fid] = int(finfo[5].split(':')[1])
            
    return qfc, sfc, lfc, afc, ftype_dict, deadline_dict, src_dict, dst_dict, size_dict 

@performance(LEVEL)
def queue_tracer(input_file_name):
    input_file = open(input_file_name, 'r')
    qrecord_list = []
    for line in input_file:
        time, server, pktcnt, size = line.strip().split(' ')
        q = Qrecord()
        q.time = int(time)
        q.rack = 0
        q.server = int(server)
        q.pktcnt = int(pktcnt)
        q.size = int(size)
        qrecord_list.append(q)
    return qrecord_list

#input: models.Simulation s, output_dir
#output: s, flow_list
@performance(LEVEL)
def get_sim_result(s, output_dir):

    qfc, sfc, lfc, afc, ftype_dict, deadline_dict, src_dict, dst_dict, size_dict = flow_tracer(input_file_name = '%s/flow.tr' % output_dir)
    s.qfc = qfc
    s.sfc = sfc
    s.lfc = lfc
    s.afc = afc
    s.save()
    #print 's = %s' % s
    #using python script now
    fid_list, stime_dict, etime_dict, drcnt_dict, thrput_dict, pktcnt_dict = packet_tracer(input_file_name = '%s/packet.tr' % output_dir)
    flow_list = []
    for fid in fid_list:
        flow = Flow()
        flow.start = int(stime_dict[fid]*1000000)
        flow.end = int(etime_dict[fid]*1000000)
        duration = flow.end - flow.start
        flow.thrput = thrput_dict[fid]
        flow.drcnt = drcnt_dict[fid]
        flow.pktcnt = pktcnt_dict[fid]
        ##
        flow.ftype = ftype_dict[fid]
        flow.deadline = deadline_dict[fid]
        flow.src = src_dict[fid]
        flow.dst = dst_dict[fid]
        flow.size = size_dict[fid]
        flow.finished = size_dict[fid] + pktcnt_dict[fid]*40 <= thrput_dict[fid]
        flow.sim = s
        flow.save()
        #print flow
        flow_list.append(flow)
    qrecord_list = queue_tracer(input_file_name = '%s/queue.tr' % output_dir)
    for q in qrecord_list:
        q.sim = s
        #q.save()
    return s, flow_list, qrecord_list
