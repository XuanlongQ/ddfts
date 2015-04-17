set FTYPE_L 0
set FTYPE_S 1
set FTYPE_Q 2
set path [file normalize [info script]]
set path [file dirname $path]
source "$path/random.tcl"
#########initial parameters#############
source "$path/init_param.tcl"
init_param

#######################
# Creating New Simulator
set ns [new Simulator]
# Setting up the traces
set flow_file [open $output_dir/flow.tr w]
set packet_file [open $output_dir/packet.tr w]
set queue_file [open $output_dir/queue.tr w]
#set tcp_file [open $output_dir/tcp.tr w]
$ns trace-all $packet_file

##topology
set sc 35
set tor [$ns node]
for {set i 0} {$i < $sc} {incr i 1} {
    set server($i) [$ns node]
    $ns simplex-link $tor $server($i) $link_bw $link_lt RED
    set queue_monitor($i) [$ns monitor-queue $tor $server($i) /tmp/queue_${i}.tr $trace_sampling_interval]
    $ns simplex-link $server($i) $tor $link_bw $link_lt DropTail
    $ns queue-limit $tor $server($i) $queue_limit
    $ns queue-limit $server($i) $tor $queue_limit
}

##traffic
set fc 0
set qfc 0
set sfc 0
set lfc 0
#query traffic: 1 pkt for request, 2 pkts for response
proc query { } {
    global ns
    global packetSize
    global sc
    global server
    global fc
    global qfc
    global qf_req_app qf_res_app
    global flow_file
    global req_count res_count
    global FTYPE_Q
    global incast_avoid

    set incast_avoid false

    set req_count 0
    set res_count 0
    set now [$ns now]
    set now [expr $now + 0.0000001]
    for {set i 1} {$i < $sc} {incr i 1} {
        incr qfc
        incr fc
        set qfid $qfc
        set fid $fc
        #Transmission Layer
        set qf_req_tcp($qfid) [new Agent/TCP/FullTcp/Sack]
        set qf_res_tcp($qfid) [new Agent/TCP/FullTcp/Sack]
        $qf_req_tcp($qfid) set d2tcp_d_ [expr 1000]
        $qf_res_tcp($qfid) set d2tcp_d_ [expr 1000]
        $qf_req_tcp($qfid) set ftype_ FTYPE_Q
        $qf_res_tcp($qfid) set ftype_ FTYPE_Q
        $ns attach-agent $server(0)  $qf_req_tcp($qfid)
        $ns attach-agent $server($i) $qf_res_tcp($qfid)
        $ns connect $qf_req_tcp($qfid) $qf_res_tcp($qfid)
        $qf_req_tcp($qfid) set fid_ $fid
        $qf_res_tcp($qfid) set fid_ $fid
        $qf_res_tcp($qfid) listen
        #Application Layer
        set qf_req_app($qfid) [new Application/TcpApp $qf_req_tcp($qfid)]
        set qf_res_app($qfid) [new Application/TcpApp $qf_res_tcp($qfid)]
        $qf_req_app($qfid) connect $qf_res_app($qfid)
        set size [expr 3 * $packetSize]
        puts $flow_file "flow:$fid|ftype:q|deadline:-1|src:0|dst:$i|size:$size"
        set size [expr 1 * $packetSize]
        $ns at $now "$qf_req_app($qfid) send $size {$qf_res_app($qfid) recv {$qfid}}"
        incr req_count
    }
}

proc avoid_incast { } {
    global incast_avoid
    global lfc
    global lf_req_tcp lf_res_tcp
    set incast_avoid true
    global K

    for {set i 1} {$i < $lfc} {incr i 1} {
        set lfid $i
        #$lf_req_tcp($lfid) set cwnd_ 1
        #$lf_res_tcp($lfid) set cwnd_ 1
        #$lf_req_tcp($lfid) set ssthresh_ 2
        #$lf_res_tcp($lfid) set ssthresh_ 2
    }

    Queue/RED set thresh_ [expr $K/4] ; #minthresh
    Queue/RED set maxthresh_ [expr $K/4] ; #maxthresh

}
set delay [expr 0.000004*($sc-1)*2]
set jitter [udr 0 $delay]
Application/TcpApp instproc recv {i} {
	global ns
    global packetSize
    global qf_req_app qf_res_app
    global req_count
    global res_count
    global jitter
    global incast_avoid
    global K

    if { $incast_avoid == false } {
        avoid_incast
    }
    set now [expr [$ns now] + 0.00000]
    set res_time [expr $now + [$jitter value]]
    set size [expr 2 * $packetSize]
    if { $i>0 } {
        $ns at $res_time "$qf_res_app($i) send $size {$qf_req_app($i) recv {-1}}"
    }
    if { $i==-1 } {
      incr res_count
      if { $res_count >= $req_count } {
        set incast_avoid true
        Queue/RED set thresh_ [expr $K] ; #minthresh
        Queue/RED set maxthresh_ [expr $K] ; #maxthresh
        $ns at [expr $now + 0.0] "query"
      }
    }
}

$ns at .0 "query"

#short (message) flow: update control state on the workers 100KB-1MB

#large flow: copy fresh data to workers 1MB-100MB
for {set i 1} {$i < $sc} {incr i 1} {
      incr lfc
      incr fc
      set lfid $lfc
      set fid $fc
      #Transmission Layer
      set lf_req_tcp($lfid) [new Agent/TCP/FullTcp/Sack]
      set lf_res_tcp($lfid) [new Agent/TCP/FullTcp/Sack]
      $ns attach-agent $server(0)  $lf_req_tcp($lfid)
      $ns attach-agent $server($i) $lf_res_tcp($lfid)
      $ns connect $lf_req_tcp($lfid) $lf_res_tcp($lfid)
      $lf_req_tcp($lfid) set fid_ $fid
      $lf_res_tcp($lfid) set fid_ $fid
      $lf_req_tcp($lfid) set ftype_ FTYPE_L
      $lf_res_tcp($lfid) set ftype_ FTYPE_L
      $lf_res_tcp($lfid) listen
      #Application Layer
      set lf_req_app($lfid) [new Application/TcpApp $lf_req_tcp($lfid)]
      set lf_res_app($lfid) [new Application/TcpApp $lf_res_tcp($lfid)]
      $lf_req_app($lfid) connect $lf_res_app($lfid)
      set size [expr 2000000000]
      puts $flow_file "flow:$fid|ftype:l|deadline:-1|src:0|dst:$i|size:$size"
      $ns at 0.0 "$lf_req_app($lfid) send $size {$lf_res_app($lfid) recv {-3}}"
}


##tracer
proc my_trace { } {

    global ns sc trace_sampling_interval queue_monitor queue_file
    set now [$ns now]
    set now_ [expr int([expr $now*1000000])]
    for {set i 0} {$i < $sc} {incr i 1} {
        $queue_monitor($i) instvar parrivals_ pdepartures_ pdrops_ bdepartures_ pkts_ size_
        #now $rack $server $queue_size_
        puts $queue_file "$now_ 0 $i $pkts_ $size_"    
    }
    $ns at [expr $now + $trace_sampling_interval] "my_trace"
}
$ns at $trace_sampling_interval "my_trace"

proc finish {} { 
    global qfc lfc fc
	global ns flow_file packet_file queue_file
	
    puts $flow_file "qfc:$qfc"
    puts $flow_file "lfc:$lfc"
    puts $flow_file "afc:$fc"
	$ns flush-trace
	#puts "Simulation completed."
	close $flow_file
	close $packet_file
	close $queue_file
	#close $tcp_file
	exit 0
}

#end
$ns at $sim_end_time "finish"
$ns run
