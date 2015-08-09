#!/usr/bin/python

import sys,os
import commands
import threading, time
from models import *
from tool import performance
LEVEL = 'DEBUG'
sim_list = []

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

#@performance(LEVEL)
def ns_simulation(sid, tcptype, sc, lfc, tcl_output_dir):
    #simulate network using tcl script
    sim = ['simulation.tcl', 'incast_simulation.tcl']
    (status, output) = commands.getstatusoutput('/home/lqx/bin/ns-allinone-2.35/bin/ns sim/simulation/%s %s %s %s %s'%(sim[1], tcptype, sc, lfc, tcl_output_dir))
    #(status, output) = commands.getstatusoutput('/home/lqx/bin/ns-allinone-2.35/bin/ns sim/simulation/%s %s %s'%(sim[0], tcptype, tcl_output_dir))
    #print 'network simulation has generated: ' + tcl_output_dir
    print status, output

#input s: model.Simulation
#output s, flow_list: model.Flow
#@performance(LEVEL)
def simulate(s):
    sid = s.sid
    tcptype = s.tcptype
    sc = s.sc
    lfc = s.lfc
    
    path = cur_file_dir()
    out_dir = '%s/sim/out/%s' % (path, sid)
    #print 'out_dir = %s' % (out_dir,)
    #return

    #(status, output) = commands.getstatusoutput('rm -rf %s/sim/out' % (path,) )
    #print status, output
    (status, output) = commands.getstatusoutput('mkdir -p %s/tcl'%(out_dir))
    #print status, output

    tcl_output_dir = '%s/tcl/'%(out_dir,) 
    #print tcl_output_dir
    t1 = time.time()
    ns_simulation(sid, tcptype, sc, lfc, tcl_output_dir)
    from sim_result import get_sim_result
    s, flow_list, qrecord_list, cwnd_list = get_sim_result(s, tcl_output_dir)
    t2 = time.time()
    s.time = t2 - t1
    #remove tcl output bucause it's too big!!
    #(status, output) = commands.getstatusoutput('rm -rf %s/tcl'%(out_dir))
    #print status, output
    #(status, output) = commands.getstatusoutput('mkdir -p %s/tcl'%(out_dir))
    #print status, output
    return s, flow_list, qrecord_list, cwnd_list

SIM_DAEMON =  None

@performance(LEVEL)
def simulate_daemon(args):
    global sim_list
    current_thread = threading.currentThread()
    while True:
            UNDONE = 0
            SIMING = 1
            DONE = 2
            #check if simulate thread is already started 
            undone = [ s for s in sim_list if s.status == UNDONE ]
            if len(undone) == 0:
                print '[At %s: %03d] There is no undone simulation now' % (current_thread, int(time.time())%100,)
            for sim in undone:
                print '[At %s: %03d] Simulate simulation %s[sc:%s, lfc:%s, %s]' \
                    % (current_thread, int(time.time())%100, sim.sid, sim.sc, sim.lfc, sim.tcptype,)
                sim.status = SIMING
                sim, flow_list, qrecord_list, cwnd_list = simulate(sim)

                sim.status = DONE
                #sim.flow_list = flow_list
                #sim.qrecord_list = qrecord_list
                #sim.cwnd_list = cwnd_list
                sim.lf_thrput = 0
                sim.qf_thrput = 0
                for f in flow_list:
                   if f.ftype == 'l':
                       sim.lf_thrput += f.thrput
                   elif f.ftype == 'q':
                       sim.qf_thrput += f.thrput
                print '[At %s: %03d] Simulation %s is finished,\n \
                    qfc = %d, qf_thrput = %d, lf_thrput = %d, thrput = %d\n\n' \
                    % (current_thread, int(time.time())%100, sim.sid, sim.qfc,\
                    sim.qf_thrput, sim.lf_thrput, (sim.qf_thrput + sim.lf_thrput),)
            time.sleep(10)

            daemon = threading.Thread(target=simulate_daemon, args=('simulate daemon',))
            daemon.setDaemon(True)
            daemon.start()
            print '[At %s: %03d] start daemon %s' % (current_thread, int(time.time())%100, daemon,)
            global SIM_DAEMON
            SIM_DAEMON = daemon
            return
    
