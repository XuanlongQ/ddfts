set my_argc 2
#argv: tcp_type, output_dir
if {$::argc < $my_argc} {
	puts "argc = $argc, but we need $my_argc arguments"
	exit
}
set i 0
set tcptype [lindex $argv $i]
	#puts "tcp_type=$tcp_type"
incr i
set output_dir [lindex $argv $i]
	#puts "output_dir=$output_dir"
incr i

#tcp type
set dctcp false
set d2tcp false
set sdnd2tcp false
if { $tcptype == "dctcp" } {
    set dctcp true
}

if { $tcptype == "d2tcp" } {
    set d2tcp true
}

if { $tcptype == "sdnd2tcp" } {
    set sdnd2tcp true
}

#topology parameters
set queue_alg DropTail
#set queue_alg RED
set K 37
set queue_limit 104 ; #incast: a static allocation of 100 packets to each port(@DCTCP)
set link_bw 1Gb
set link_lt 20us

#trace parameters
set trace_sampling_interval 0.00005

#simulation end time
set sim_end_time .81

set packetSize 1460

proc init_param { } {

    global dctcp d2tcp sdnd2tcp
    global packetSize
    global K
    global queue_alg

    set DCTCP_g_  [expr 1.0/16]; #@DCTCP 1.0/16
    set ackRatio 1 

    Agent/TCP set ecn_ 1
    Agent/TCP set old_ecn_ 1
    Agent/TCP set packetSize_ $packetSize
    Agent/TCP/FullTcp set segsize_ $packetSize
    Agent/TCP set window_ 1256
    Agent/TCP set slow_start_restart_ false
    Agent/TCP set tcpTick_ 0.01; #clock granularity
    Agent/TCP set minrto_ 0.3 ; # minRTO = 300ms
    Agent/TCP set windowOption_ 0


    if { $dctcp } {
        puts "enable dctcp!!!"
        set queue_alg RED
        Agent/TCP set dctcp_ true
        Agent/TCP set dctcp_g_ $DCTCP_g_; #g is the weight given to new samples against the past in the estimation of alpha
        Agent/TCP set dctcp_alpha_ 0; # alpha = (1-g)*alpha + g*F, alpha is an estimate of the fraction of packets that are marked
                                      #where F is the fraction of 
                                      #packets that were marked in the last window of data
    }

    if { $d2tcp } {
        puts "enable d2tcp!!!"
        set queue_alg RED
        Agent/TCP set dctcp_ true
        Agent/TCP set dctcp_g_ $DCTCP_g_; 
        Agent/TCP set dctcp_alpha_ 0; 
        Agent/TCP set d2tcp_ true
        Agent/TCP set dctcp_d_ 1; 
    }

    if { $sdnd2tcp } {
        puts "enable sdnd2tcp!!!"
        set queue_alg RED
        Agent/TCP set dctcp_ true
        Agent/TCP set dctcp_g_ $DCTCP_g_; 
        Agent/TCP set dctcp_alpha_ 0; 
        Agent/TCP set d2tcp_ true
        Agent/TCP set dctcp_d_ 1; 
        Agent/TCP set sdn_ true
    }
    Agent/TCP/FullTcp set segsperack_ $ackRatio; #for window updates
    Agent/TCP/FullTcp set spa_thresh_ 3000; # rcv_nxt < spa_thresh_? -> 1 seg per ack
    Agent/TCP/FullTcp set interval_ 0.04 ; #delayed ACK interval = 40ms

    Queue set limit_ 1000

    Queue/RED set bytes_ false ; #use bytes?
    Queue/RED set queue_in_bytes_ true ; #q in bytes?
    Queue/RED set mean_pktsize_ $packetSize
    Queue/RED set setbit_ true ; #mark instead of drop
    Queue/RED set gentle_ false
    Queue/RED set q_weight_ 1.0 ; #1.0 means that use current queue length but not average queue length
    Queue/RED set mark_p_ 1.0
    #puts "set thresh_"
    Queue/RED set thresh_ [expr $K] ; #minthresh
    Queue/RED set maxthresh_ [expr $K] ; #maxthresh
                 
    DelayLink set avoidReordering_ true
}
