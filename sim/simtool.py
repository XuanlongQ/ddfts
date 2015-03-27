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


    from sim_result import get_sim_result

    tcl_output_dir = '%s/tcl/'%(out_dir,) 
    #print tcl_output_dir

    #simulate network using tcl script
    (status, output) = commands.getstatusoutput('/home/lqx/bin/ns-allinone-2.35/bin/ns sim/simulation/simulation.tcl %s %s %s'%(sid, dctcp, tcl_output_dir))
    print 'network simulation has generated: ' + tcl_output_dir
    print status, output

    s, flow_list = get_sim_result(s, tcl_output_dir)

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
    
