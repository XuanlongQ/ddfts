#!/usr/bin/python
		#test_id dctcp RTT queue_limit
#ns simulation.tcl T001 true 17 250
dctcp = ('true', 'false')
RTT = (13, 17)
queue_limit = (128, 250)
dl = len(dctcp)
rl = len(RTT) 
ll = len(queue_limit)
dctcp_list = []
RTT_list =  []

for d in dctcp:
    dctcp_list += [d]*(rl*ll)
for r in RTT:
    RTT_list += [r]*ll
RTT_list *= dl
queue_limit_list =  queue_limit*(dl*rl)

import time
now = time.strftime('%y%m%d-%H%M%S', time.localtime(time.time()))
tid = 'T-%s'%now
out_dir = 'out/%s'%tid
tcl_out_dir = '%s/tcl'%out_dir
import commands
(status, output) = commands.getstatusoutput('mkdir -p %s'%(tcl_out_dir))
print status, output
awk_out_dir = '%s/awk'%out_dir
(status, output) = commands.getstatusoutput('mkdir -p %s'%(awk_out_dir))
print status, output
plt_out_dir = '%s/plt'%out_dir
(status, output) = commands.getstatusoutput('mkdir -p %s'%(plt_out_dir))
print status, output
for dctcp, RTT, queue_limit in zip(dctcp_list, RTT_list, queue_limit_list):
    output_tr = '%s/%s_%s_%s.tr'%(tcl_out_dir, dctcp, RTT, queue_limit)
    print output_tr
    output_dat = '%s/%s_%s_%s.dat'%(awk_out_dir, dctcp, RTT, queue_limit)
    print output_dat
    output_plt = '%s/%s_%s_%s.jpg'%(plt_out_dir, dctcp, RTT, queue_limit)
    print output_plt
    import commands
    #run tcl script
    (status, output) = commands.getstatusoutput('ns simulation.tcl %s %s %s %s'%(tid, dctcp, RTT, queue_limit))
    print status, output
    #run awk script
    (status, output) = commands.getstatusoutput('awk -f measure_flow_delay.awk %s > %s'%(output_tr, output_dat))
    print status, output
    #run plt script
    (status, output) = commands.getstatusoutput('python plot_flow_delay.py %s'%(output_dat))
    print status, output

