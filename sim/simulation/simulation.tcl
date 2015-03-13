set my_argc 3
#argv: test_id, dctcp, tcl_output
if {$::argc < $my_argc} {
	puts "argc = $argc, but we need $my_argc arguments"
	exit
}
#test id
set i 0
set tid [lindex $argv $i]
	puts "test_id=$tid"
incr i
set dctcp [lindex $argv $i]
	puts "dctcp=$dctcp"
incr i
set tcl_output [lindex $argv $i]
	puts "tcl_output=$tcl_output"
incr i

set RTT 200
set queue_limit 250

##############
# Creating New Simulator
set ns [new Simulator]

#######################
# Setting up the traces
set f [open $tcl_output w]
$ns trace-all $f
proc finish {} { 
	global ns f namtrace
	
	$ns flush-trace
	puts "Simulation completed."
	close $f
	exit 0
}

#uniform distribution random
proc udr {min max} {
	set rng [new RNG]
	$rng seed 1
	set r [new RandomVariable/Uniform]
	$r use-rng $rng
	$r set min_ $min
	$r set max_ $max
	return $r

}
proc prr {avg shape} {
	set rng [new RNG]
	$rng seed 1
	set r [new RandomVariable/Pareto]
	$r use-rng $rng
	$r set avg_ $avg
	$r set shape_ $shape
	return $r

}
proc start_flow {i t} {

	global ns
	global sf_fid sf_src sf_dst sf_size sf_start sf_end sf_tcp sf_sink sf_ftp
    global ${t}f_fid
    global ${t}f_src ${t}f_dst ${t}f_size
    global ${t}f_start ${t}f_end
    global ${t}f_tcp ${t}f_sink ${t}f_ftp

	eval "set fid \$${t}f_fid($i)"
	eval "set src \$${t}f_src($i)"
	eval "set dst \$${t}f_dst($i)"
	eval "set size \$${t}f_size($i)"
	eval "set start \$${t}f_start($i)"
	eval "set tcp \$${t}f_tcp($i)"
	eval "set sink \$${t}f_sink($i)"
	eval "set ftp \$${t}f_ftp($i)"

	$ns attach-agent $src $tcp
	$ns attach-agent $dst $sink
	$ns connect $tcp $sink
	$tcp set fid_ $fid

	#ftp
	$ftp attach-agent $tcp
	$ftp set type_ FTP
	
	if { $start > 0 && $size > 0} {
		$ns at $start "$ftp send $size"
		#puts "flow $i\[[$src id]->[$dst id]\] start at $start and the size is $size"
	}
}
##############
set sourceAlg DC-TCP-Sack
set switchAlg RED
set lineRate 10Gb
set inputLineRate 11Gb

set DCTCP_g_ 0.0625
set ackRatio 1 
set packetSize 1460

Agent/TCP set ecn_ 1
Agent/TCP set old_ecn_ 1
Agent/TCP set packetSize_ $packetSize
Agent/TCP/FullTcp set segsize_ $packetSize
Agent/TCP set window_ 1256
Agent/TCP set slow_start_restart_ false
Agent/TCP set tcpTick_ 0.01
Agent/TCP set minrto_ 0.2 ; # minRTO = 200ms
Agent/TCP set windowOption_ 0


if {[string compare $sourceAlg "DC-TCP-Sack"] == 0} {
    Agent/TCP set dctcp_ $dctcp
    Agent/TCP set dctcp_g_ $DCTCP_g_;
}
Agent/TCP/FullTcp set segsperack_ $ackRatio; 
Agent/TCP/FullTcp set spa_thresh_ 3000;
Agent/TCP/FullTcp set interval_ 0.04 ; #delayed ACK interval = 40ms

Queue set limit_ 1000

Queue/RED set bytes_ false
Queue/RED set queue_in_bytes_ true
Queue/RED set mean_pktsize_ $packetSize
Queue/RED set setbit_ true
Queue/RED set gentle_ false
Queue/RED set q_weight_ 1.0
Queue/RED set mark_p_ 1.0
set K 65
Queue/RED set thresh_ [expr $K]
Queue/RED set maxthresh_ [expr $K]
			 
DelayLink set avoidReordering_ true

#####################################
$ns color 0 Blue
$ns color 1 Red
$ns color 2 Green
$ns color 3 Yellow
$ns color 4 Purple
$ns color 5 White
$ns color 6 Orange
$ns color 7 Violet
$ns color 8 Brown
$ns color 9 Black


#flow
#fid, start, end, size, src, dst, 
#query flow: 1.6-2KB
#qf_
#short (message) flow: 50KB-1MB
#sf_
#large flow: 1MB-100MB
#lf_

#server group: sg
set sg 1
#server count sc
set sc 4

#flow count fc
set fc 0

#simulation end time
set sim_end_time 10.0

#time unit: second
set t_unit 0.001

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
		$ns simplex-link $server($i,$j) $rack($i) 1000Mb .020ms DropTail
		$ns queue-limit $rack($i) $server($i,$j) $queue_limit
		$ns queue-limit $server($i,$j) $rack($i) $queue_limit
		$ns duplex-link-op $server($i,$j) $rack($i) queuePos 0.5
	}
}

#query traffic
source query_flow.tcl
setup_query_flow

#short (message) flow: update control state on the workers 100KB-1MB
source short_flow.tcl
setup_short_flow

#large flow: copy fresh data to workers 1MB-100MB
source large_flow.tcl
setup_large_flow

$ns at $sim_end_time "finish"

$ns run
