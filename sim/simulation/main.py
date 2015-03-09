#!/usr/bin/python
		#test_id dctcp RTT queue_limit
#ns simulation.tcl T001 true 17 250
DEBUG = True
dctcp_list = ('true', 'false')
RTT_list = (13, 17)
queue_limit_list = (128, 250)
RTT_list = (13,)
queue_limit_list = (128,)

import time
now = time.strftime('%y%m%d-%H%M%S', time.localtime(time.time()))
tid = 'T-%s'%now
out_dir = 'out/%s'%tid

import commands
(status, output) = commands.getstatusoutput('rm -rf out')
DEBUG and print status, output
tcl_out_dir = '%s/tcl'%out_dir
(status, output) = commands.getstatusoutput('mkdir -p %s'%(tcl_out_dir))
DEBUG and print status, output
awk_out_dir = '%s/awk'%out_dir
(status, output) = commands.getstatusoutput('mkdir -p %s'%(awk_out_dir))
DEBUG and print status, output
plt_out_dir = '%s/plt'%out_dir
(status, output) = commands.getstatusoutput('mkdir -p %s'%(plt_out_dir))
DEBUG and print status, output


from plot_flow_delay import plot_flow_delay
for RTT in RTT_list:
    for queue_limit in queue_limit_list:
        plt_input_list = []
        plt_output = RTT + '_' + queue_limit + '.png'
        label_dict = {}
        for dctcp in dctcp_list:
            sim_args = '%s/%s_%s_%s'%(tcl_out_dir, dctcp, RTT, queue_limit)

            tcl_output = sim_args + '.tr'
            DEBUG and print tcl_output
            awk_output =  + '.dat'
            DEBUG and print awk_output
            DEBUG and print plt_output

            plt_input = awk_output
            plt_input_list += [ plt_input, ]
            label_dict[plt_input] = sim_args

            #simulate network using tcl
            #run tcl script
            (status, output) = commands.getstatusoutput('ns simulation.tcl %s %s %s %s'%(tid, dctcp, RTT, queue_limit))
            print status, output
            #calculate flow delay using awk
            #run awk script
            (status, output) = commands.getstatusoutput('awk -f measure_flow_delay.awk %s > %s'%(tcl_output, awk_output))
            print status, output
        #plot flow delay using python
        plot_flow_delay(plt_input_list, label_dict = label_dict, plt_output = plt_output)
