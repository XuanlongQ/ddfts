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
#output flow_list: model.Flow
def simulate(s):
    sid = s.sid
    dctcp = 'true' if s.dctcp else 'false'
    
    path = cur_file_dir()
    out_dir = '%s/sim/simulation/out/%s' % (path, sid)
    print 'out_dir = %s' % (out_dir,)
    #return

    import commands
    (status, output) = commands.getstatusoutput('rm -rf %s/sim/simulation/out' % (path,) )
    #print status, output
    (status, output) = commands.getstatusoutput('mkdir -p %s/tcl'%(out_dir))
    #print status, output
    (status, output) = commands.getstatusoutput('mkdir -p %s/awk'%(out_dir))
    #print status, output
    (status, output) = commands.getstatusoutput('mkdir -p %s/plt'%(out_dir))
    #print status, output


    from simulation.plot_flow_delay import plot_flow_delay
    from simulation.analyse_flow import analyse_flow

    plt_input_list = []
    plt_output =  '%s/plt/%s.png'%(out_dir, dctcp) 
    label_dict = {}
    sim_args = '%s'%(dctcp,)
    tcl_output = '%s/tcl/%s.tr'%(out_dir, sim_args) 
    #print tcl_output
    awk_output = '%s/awk/%s.dat'%(out_dir, sim_args)
    #print awk_output
    plt_input = awk_output
    plt_input_list += [ plt_input, ]
    label_dict[plt_input] = sim_args
    #simulate network using tcl
    #run tcl script
    (status, output) = commands.getstatusoutput('/home/lqx/bin/ns-allinone-2.35/bin/ns sim/simulation/simulation.tcl %s %s %s'%(sid, dctcp, tcl_output))
    print 'network simulation has generated: ' + tcl_output
    print status, output
    #using python script now
    fid_list, stime_dict, etime_dict, drcnt_dict, thrput_dict = analyse_flow(input_file_name = tcl_output, output_file_name = awk_output)
    from models import Flow
    for fid in fid_list:
        flow = Flow()
        flow.start = stime_dict[fid]
        flow.end = etime_dict[fid]
        duration = flow.end - flow.start
        flow.thrput = thrput_dict[fid]
        flow.drcnt = drcnt_dict[fid]
        ##
        flow.ftype = 's'
        flow.deadline = duration
        flow.src = 1
        flow.dst = 2
        flow.size = thrput_dict[fid]
        flow.finished = True
        flow.save()
    print 'has calculated flow: ' + awk_output
    '''
    #plot flow delay using python
    #print plt_input_list
    #print label_dict
    plot_flow_delay(plt_input_list, label_dict = label_dict, plt_output = plt_output)
    print 'plot flow delay: ' + plt_output
    '''
    #remove tcl output bucause it's to big!!
    (status, output) = commands.getstatusoutput('rm -rf %s/tcl'%(out_dir))
    #print status, output
    (status, output) = commands.getstatusoutput('mkdir -p %s/tcl'%(out_dir))
    #print status, output

if __name__ == '__main__':
    from models import Simulation, Flow
    s = Simulation()
    s.sid = 'S001'
    s.dctcp = False
    s.done = False
    simulate(s)
