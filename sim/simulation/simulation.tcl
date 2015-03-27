set my_argc 3
#argv: test_id, dctcp, output_dir
if {$::argc < $my_argc} {
	puts "argc = $argc, but we need $my_argc arguments"
	exit
}
#simulation id
set i 0
set sid [lindex $argv $i]
	#puts "simulation_id=$sid"
incr i
set dctcp [lindex $argv $i]
	#puts "dctcp=$dctcp"
incr i
set output_dir [lindex $argv $i]
	#puts "output_dir=$output_dir"
incr i

set RTT 200
set queue_limit 250
set trace_sampling_interval 0.01

#######################
# Creating New Simulator
set ns [new Simulator]
# Setting up the traces
set flow_file [open $output_dir/flow.tr w]
set packet_file [open $output_dir/packet.tr w]
set queue_file [open $output_dir/queue.tr w]
$ns trace-all $packet_file
proc finish {} { 
	global ns flow_file packet_file queue_file
	
	$ns flush-trace
	#puts "Simulation completed."
	close $flow_file
	close $packet_file
	close $queue_file
	exit 0
}
###setup tcp#####################
set path [file normalize [info script]]
set path [file dirname $path]
source "$path/setup_tcp.tcl"
####################################

#server group: sg
set sg 1
#server count sc
set sc 14

#simulation end time
set sim_end_time 10.0

#fid, start, end, size, src, dst, 
#query flow: 1.6-2KB, qf_
#short (message) flow: 50KB-1MB, sf_
#large flow: 1MB-100MB, lf_
#flow count fc
set fc 0
#query flow count qfc
set qfc [expr 2000*$sg*$sc]
#short (message) flow count
set sfc [expr 200*$sg*$sc]
#large flow count
set lfc 100

#set topology
for {set i 0} {$i < $sg} {incr i 1} {
	#
	#Create Nodes
	#
	set rack($i) [$ns node]
      		#puts "rack([expr $i]): [$rack($i) id]"
	for {set j 0} {$j < $sc} {incr j 1} {
		set server($i,$j) [$ns node]
      			#puts "server([expr $i],[expr $j]): [$server($i,$j) id]"
		$ns simplex-link $rack($i) $server($i,$j) 1000Mb .020ms RED
        set queue_monitor($i,$j) [$ns monitor-queue $rack($i) $server($i,$j) /tmp/queue_${i}_$j.tr $trace_sampling_interval]
		$ns simplex-link $server($i,$j) $rack($i) 1000Mb .020ms DropTail
		$ns queue-limit $rack($i) $server($i,$j) $queue_limit
		$ns queue-limit $server($i,$j) $rack($i) $queue_limit
		$ns duplex-link-op $server($i,$j) $rack($i) queuePos 0.5
	}
}

source "$path/trace.tcl"

#######################
source "$path/random.tcl"
#######################
#start flow
source "$path/start_flow.tcl"

#query traffic
source "$path/query_flow.tcl"
setup_query_flow

#short (message) flow: update control state on the workers 100KB-1MB
source "$path/short_flow.tcl"
setup_short_flow

#large flow: copy fresh data to workers 1MB-100MB
source "$path/large_flow.tcl"
setup_large_flow

puts "afc:$fc"

$ns at $trace_sampling_interval "my_trace"
$ns at $sim_end_time "finish"
$ns run
