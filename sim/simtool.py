#!/usr/bin/python

import sys,os

def cur_file_dir():
    path = sys.path[0]
    #print 'path = %s' % (path,)
    #print 'path.dirname = %s' % (os.path.dirname(path),)
    return path
    '''
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)
    '''
def get_flow_info(input_line_list):
    input_line_list = input_line_list.strip().split('\n')
    qfc, sfc, lfc, afc = (0, 0, 0, 0)
    ftype_dict = {}
    deadline_dict = {}
    src_dict = {}
    dst_dict = {}
    size_dict = {}
    #print 'get flow info'
    #print len(input_line_list)
    for line in input_line_list:
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

#input s: model.Simulation
#output s, flow_list: model.Flow
def simulate(s):
    sid = s.sid
    dctcp = 'true' if s.dctcp else 'false'
    
    path = cur_file_dir()
    out_dir = '%s/sim/out/%s' % (path, sid)
    print 'out_dir = %s' % (out_dir,)
    #return

    import commands
    (status, output) = commands.getstatusoutput('rm -rf %s/sim/out' % (path,) )
    #print status, output
    (status, output) = commands.getstatusoutput('mkdir -p %s/tcl'%(out_dir))
    #print status, output


    from analyse_flow import analyse_flow

    sim_args = '%s'%(dctcp,)
    tcl_output = '%s/tcl/%s.tr'%(out_dir, sim_args) 
    #print tcl_output

    #simulate network using tcl script
    (status, output) = commands.getstatusoutput('/home/lqx/bin/ns-allinone-2.35/bin/ns sim/simulation/simulation.tcl %s %s %s'%(sid, dctcp, tcl_output))
    print 'network simulation has generated: ' + tcl_output
    #print status, output
    qfc, sfc, lfc, afc, ftype_dict, deadline_dict, src_dict, dst_dict, size_dict = get_flow_info(output)
    s.qfc = qfc
    s.sfc = sfc
    s.lfc = lfc
    s.afc = afc
    s.save()
    #print 's = %s' % s
    #using python script now
    fid_list, stime_dict, etime_dict, drcnt_dict, thrput_dict, pktcnt_dict = analyse_flow(input_file_name = tcl_output)
    from models import Flow
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

    #remove tcl output bucause it's to big!!
    (status, output) = commands.getstatusoutput('rm -rf %s/tcl'%(out_dir))
    #print status, output
    (status, output) = commands.getstatusoutput('mkdir -p %s/tcl'%(out_dir))
    #print status, output
    return s, flow_list

SIM_DAEMON =  None

def simulate_daemon(args):
    from models import Simulation, Flow
    import threading, time
    current_thread = threading.currentThread()
    while True:
            UNDONE = 0
            SIMING = 1
            DONE = 2
            #check if simulate thread is already started 
            #print 'len(siming):', len(siming)
            undone = Simulation.objects.filter(status=UNDONE) 
            if len(undone) == 0:
                print '[At %s: %s]there is no undone simulation now' % (current_thread, time.time())
            for sim in undone:
                print '[At %s: %s]simulate simulation ' % (current_thread, time.time()), sim.sid
                sim.status = SIMING
                sim.save()
                sim, flow_list = simulate(sim)
                sim.status = DONE
                sim.save()
                print '[At %s: %s]simulation %s is finished' % (current_thread, time.time(), sim.sid,)
            import time
            time.sleep(5)
    
