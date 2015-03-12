#!/usr/bin/python
		#test_id dctcp RTT queue_limit
#ns simulation.tcl T001 true 17 250
DEBUG = True
dctcp_list = ('true', 'false')
RTT_list = (200,)
queue_limit_list = (250,)

import time
now = time.strftime('%y%m%d-%H%M%S', time.localtime(time.time()))
tid = 'T-%s'%now
out_dir = 'out/%s'%tid

import commands
(status, output) = commands.getstatusoutput('rm -rf out')
#print status, output
(status, output) = commands.getstatusoutput('mkdir -p %s/tcl'%(out_dir))
#print status, output
(status, output) = commands.getstatusoutput('mkdir -p %s/awk'%(out_dir))
#print status, output
(status, output) = commands.getstatusoutput('mkdir -p %s/plt'%(out_dir))
#print status, output


from plot_flow_delay import plot_flow_delay
for RTT in RTT_list:
    for queue_limit in queue_limit_list:
        plt_input_list = []
        plt_output =  '%s/plt/%03d_%04d.png'%(out_dir, RTT, queue_limit) 
        label_dict = {}
        for dctcp in dctcp_list:
            sim_args = '%s_%s_%s'%(dctcp, RTT, queue_limit)

            tcl_output = '%s/tcl/%s.tr'%(out_dir, sim_args) 
            #print tcl_output
            awk_output = '%s/awk/%s.dat'%(out_dir, sim_args)
            #print awk_output

            plt_input = awk_output
            plt_input_list += [ plt_input, ]
            label_dict[plt_input] = sim_args

            #simulate network using tcl
            #run tcl script
            (status, output) = commands.getstatusoutput('ns simulation.tcl %s %s %s'%(tid, dctcp, tcl_output))
            print 'network simulation generate: ' + tcl_output
            #print status, output
            #calculate flow delay using awk
            #run awk script
            (status, output) = commands.getstatusoutput('awk -f measure_flow_delay.awk %s > %s'%(tcl_output, awk_output))
            print 'calculate flow delay: ' + awk_output
            #print status, output
        #plot flow delay using python
        #print plt_input_list
        #print label_dict
        plot_flow_delay(plt_input_list, label_dict = label_dict, plt_output = plt_output)
        print 'plot flow delay: ' + plt_output

        #remove tcl output bucause it's to big!!
        (status, output) = commands.getstatusoutput('rm -rf %s/tcl'%(out_dir))
        #print status, output
        (status, output) = commands.getstatusoutput('mkdir -p %s/tcl'%(out_dir))
        #print status, output
