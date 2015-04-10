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
set sc 44
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
    for {set i 1} {$i < $sc} {incr i 1} {
      incr qfc
      incr fc
      set index $qfc
      set fid $fc
      #Transmission Layer
      set qf_req_tcp($index) [new Agent/TCP/FullTcp/Sack]
      set qf_res_tcp($index) [new Agent/TCP/FullTcp/Sack]
      $ns attach-agent $server(0) $qf_req_tcp($index)
      $ns attach-agent $server($i) $qf_res_tcp($index)
      $ns connect $qf_req_tcp($index) $qf_res_tcp($index)
      $qf_req_tcp($index) set fid_ $fid
      $qf_res_tcp($index) set fid_ $fid
      $qf_res_tcp($index) listen
      #Application Layer
      set qf_req_app($index) [new Application/TcpApp $qf_req_tcp($index)]
      set qf_res_app($index) [new Application/TcpApp $qf_res_tcp($index)]
      $qf_req_app($index) connect $qf_res_app($index)
      set size [expr 3 * $packetSize]
      puts $flow_file "flow:$fid|ftype:q|deadline:-1|src:0|dst:$i|size:1"
      set now [$ns now]
      $ns at now "$qf_req_app($index) send $size {$qf_res_app($index) recv {$index}}"
    }
}

Application/TcpApp instproc recv {i} {
	global ns
    global qf_req_app qf_res_app
    if { $i>0 } {
        $ns at [$ns now] "$qf_res_app($i) send 2000 {$qf_req_app($i) recv {-1}}"
    }
    if { $i<0 } {
    }
}

query

#short (message) flow: update control state on the workers 100KB-1MB

#large flow: copy fresh data to workers 1MB-100MB

puts $flow_file "afc:$fc"

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
	global ns flow_file packet_file queue_file
	
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
