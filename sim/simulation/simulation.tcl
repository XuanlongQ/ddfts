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

#set topology
#server group: sg
set sg 1
#server count sc
set sc 35

for {set i 0} {$i < $sg} {incr i 1} {
	#
	#Create Nodes
	#
	set rack($i) [$ns node]
      		#puts "rack([expr $i]): [$rack($i) id]"
	for {set j 0} {$j < $sc} {incr j 1} {
		set server($i,$j) [$ns node]
      			#puts "server([expr $i],[expr $j]): [$server($i,$j) id]"
		$ns simplex-link $rack($i) $server($i,$j) $link_bw $link_lt RED
        set queue_monitor($i,$j) [$ns monitor-queue $rack($i) $server($i,$j) /tmp/queue_${i}_$j.tr $trace_sampling_interval]
		$ns simplex-link $server($i,$j) $rack($i) $link_bw $link_lt DropTail
		$ns queue-limit $rack($i) $server($i,$j) $queue_limit
		$ns queue-limit $server($i,$j) $rack($i) $queue_limit
		$ns duplex-link-op $server($i,$j) $rack($i) queuePos 0.5
	}
}


#fid, start, end, size, src, dst, 
#query flow: 1.6-2KB, qf_
#short (message) flow: 50KB-1MB, sf_
#large flow: 1MB-100MB, lf_
set fc 0
set qfc 0
set sfc 0
set lfc 0
#query traffic
source "$path/query_flow.tcl"
setup_query_flow

#short (message) flow: update control state on the workers 100KB-1MB
source "$path/short_flow.tcl"
setup_short_flow

#large flow: copy fresh data to workers 1MB-100MB
source "$path/large_flow.tcl"
setup_large_flow

puts $flow_file "afc:$fc"

source "$path/trace.tcl"
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

$ns at $sim_end_time "finish"
$ns run
