set FTYPE_L 0
set FTYPE_S 1
set FTYPE_Q 2
set path [file normalize [info script]]
set path [file dirname $path]
source "$path/random.tcl"
#########initial parameters#############
source "$path/init_param.tcl"
init_param
puts "queue algorithm: $queue_alg"

#######################
# Creating New Simulator
set ns [new Simulator]
# Setting up the traces
set flow_file [open $output_dir/flow.tr w]
set packet_file [open $output_dir/packet.tr w]
set queue_file [open $output_dir/queue.tr w]
set tcp_file [open $output_dir/tcp.tr w]
$ns trace-all $packet_file

##topology
set sc 35
set tor [$ns node]
for {set i 0} {$i < $sc} {incr i 1} {
    set server($i) [$ns node]
    $ns simplex-link $tor $server($i) $link_bw $link_lt $queue_alg
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
set req_pkts 1
set res_pkts 2
#query traffic: 1 pkt for request, 2 pkts for response
proc query { } {
    global ns
    global packetSize
    global sc
    global server
    global fc
    global qfc
    global qf_req_tcp qf_res_tcp
    global qf_req_app qf_res_app
    global flow_file
    global req_count res_count
    global FTYPE_Q
    global incast_avoid
    global req_pkts res_pkts

    set incast_avoid false

    set req_count 0
    set res_count 0
    set now [$ns now]
    set now [expr $now + 0.0000001]
    for {set i 1} {$i < $sc} {incr i 1} {
        incr qfc
        incr fc
        #for recv function, qfid start with 1, not 0
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
        set size [expr ($req_pkts + $res_pkts) * $packetSize]
        puts $flow_file "flow:$fid|ftype:q|deadline:-1|src:0|dst:$i|size:$size"
        set size [expr $req_pkts * $packetSize]
        $ns at $now "$qf_req_app($qfid) send $size {$qf_res_app($qfid) recv {$qfid}}"
        incr req_count
    }
}

proc avoid_incast { } {
    global incast_avoid
    global lfc
    global lf_req_tcp lf_res_tcp
    set incast_avoid true
    global sdnd2tcp
    global K

    for {set i 1} {$i < $lfc} {incr i 1} {
        set lfid $i
        #$lf_req_tcp($lfid) set cwnd_ 1
        #$lf_res_tcp($lfid) set cwnd_ 1
        #$lf_req_tcp($lfid) set ssthresh_ 2
        #$lf_res_tcp($lfid) set ssthresh_ 2
    }

    #Queue/RED set thresh_ [expr $K/4] ; #minthresh
    #Queue/RED set maxthresh_ [expr $K/4] ; #maxthresh
    if { $sdnd2tcp } {
        #puts "set thresh 3"
        Queue/RED set thresh_ [expr 3] ; #minthresh
        Queue/RED set maxthresh_ [expr 3] ; #maxthresh
    }

}
set delay [expr 0.000004*($sc-1)*2]
set jitter [udr 0 $delay]
set INT_MIN -1000000000
Application/TcpApp instproc recv {i} {
	global ns
    global packetSize
    global qf_req_tcp qf_res_tcp
    global qf_req_app qf_res_app
    global req_count
    global res_count
    global jitter
    global incast_avoid
    global K
    global INT_MIN
    global req_pkts res_pkts

    if { $incast_avoid == false } {
        avoid_incast
    }
    set now [expr [$ns now] + 0.00000]
    set res_time [expr $now + [$jitter value]]
    set res_time [expr $now + 0.05]
    set size [expr $res_pkts * $packetSize]
    if { $i>0 } {
        set ii [expr -$i]
        $ns at $res_time "$qf_res_app($i) send $size {$qf_req_app($i) recv {$ii}}"
    }
    if { $i<0 && $i>$INT_MIN } {
      incr res_count
      if { $res_count >= $req_count } {
        set incast_avoid true
        #set cwnd_ 0 for tcp_trace
        set ii [expr -$i]
        $qf_req_tcp($ii) set cwnd_ 0
        $qf_res_tcp($ii) set cwnd_ 0
        Queue/RED set thresh_ [expr $K] ; #minthresh
        Queue/RED set maxthresh_ [expr $K] ; #maxthresh
        $ns at [expr $now + 0.01] "query"
      }
    }
}

$ns at .0 "query"

#short (message) flow: update control state on the workers 100KB-1MB

#large flow: copy fresh data to workers 1MB-100MB
for {set i 1} {$i < $sc} {incr i 4} {
      #lfid start with 0
      set lfid $lfc
      set fid $fc
      incr lfc
      incr fc
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
      $ns at 0.0 "$lf_req_app($lfid) send $size {$lf_res_app($lfid) recv {$INT_MIN}}"
}


##tracer
source "$path/trace.tcl"
$ns at $trace_sampling_interval "tcp_trace"
$ns at $trace_sampling_interval "queue_trace"

proc finish {} { 
    global qfc lfc fc
	global ns flow_file packet_file queue_file tcp_file
	
    puts $flow_file "qfc:$qfc"
    puts $flow_file "lfc:$lfc"
    puts $flow_file "afc:$fc"
	$ns flush-trace
	#puts "Simulation completed."
	close $flow_file
	close $packet_file
	close $queue_file
	close $tcp_file
	exit 0
}

#end
$ns at $sim_end_time "finish"
$ns run
