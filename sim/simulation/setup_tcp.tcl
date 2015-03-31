set DCTCP_g_ 0.0625
set ackRatio 1 
set packetSize 1460
set ftpPkgSize 1000

Agent/TCP set ecn_ 1
Agent/TCP set old_ecn_ 1
Agent/TCP set packetSize_ $packetSize
Agent/TCP/FullTcp set segsize_ $packetSize
Agent/TCP set window_ 1256
Agent/TCP set slow_start_restart_ false
Agent/TCP set tcpTick_ 0.01
Agent/TCP set minrto_ 0.2 ; # minRTO = 200ms
Agent/TCP set windowOption_ 0


if { $dctcp } {
    puts "enable dctcp!!!"
    Agent/TCP set dctcp_ true
    Agent/TCP set dctcp_g_ $DCTCP_g_; #g is the weight given to new samples against the past in the estimation of alpha
    Agent/TCP set dctcp_alpha_ 0; # alpha = (1-g)*alpha + g*F, alpha is an estimate of the fraction of packets that are marked
                                  #where F is the fraction of 
                                  #packets that were marked in the last window of data
}
if { $d2tcp } {
    puts "enable d2tcp!!!"
    Agent/TCP set dctcp_ true
    Agent/TCP set dctcp_g_ $DCTCP_g_; 
    Agent/TCP set dctcp_alpha_ 0; 
    Agent/TCP set d2tcp_ true
    Agent/TCP set dctcp_d_ 1; 
}
Agent/TCP/FullTcp set segsperack_ $ackRatio; 
Agent/TCP/FullTcp set spa_thresh_ 3000;
Agent/TCP/FullTcp set interval_ 0.04 ; #delayed ACK interval = 40ms

Queue set limit_ 1000

Queue/RED set bytes_ false ; #use bytes?
Queue/RED set queue_in_bytes_ true ; #q in bytes?
Queue/RED set mean_pktsize_ $packetSize
Queue/RED set setbit_ true ; #mark instead of drop
Queue/RED set gentle_ false
Queue/RED set q_weight_ 1.0 ; #1.0 means that use current queue length but not average queue length
Queue/RED set mark_p_ 1.0
set K 65
Queue/RED set thresh_ [expr $K] ; #minthresh
Queue/RED set maxthresh_ [expr $K] ; #maxthresh
			 
DelayLink set avoidReordering_ true
