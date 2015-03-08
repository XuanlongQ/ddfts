set namtrace false
set my_argc 4 
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
set RTT [lindex $argv $i]
	puts "RTT=$RTT"
incr i
set queue_limit [lindex $argv $i]
	puts "queue_limit=$queue_limit"
incr i
set output_dir "out/$tid/tcl"
set out_tr_file_name "${output_dir}/${dctcp}_${RTT}_${queue_limit}.tr"
	puts "out tr file name: $out_tr_file_name"
set out_nam_file_name "${output_dir}/${dctcp}_${RTT}_${queue_limit}.nam"
	puts "out nam file name: $out_nam_file_name"

##############
# Creating New Simulator
set ns [new Simulator]

#######################
# Setting up the traces
exec mkdir -p $output_dir
set f [open $out_tr_file_name w]
$ns trace-all $f
if { $namtrace } {
	set nf [open $out_nam_file_name w]
	$ns namtrace-all $nf
}
proc finish {} { 
	global ns f namtrace
	
	$ns flush-trace
	#puts "Simulation completed."
	close $f
	if { $namtrace } {
		global nf
		close $nf
	}
	#exec nam out.nam &
	exit 0
}

set N 8
set B 250
set K 65
set RTT 0.0001

set simulationTime 1.0

set startMeasurementTime 1
set stopMeasurementTime 2
set flowClassifyTime 0.001

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
proc start_flow {i} {

	global ns
	global sf_fid sf_src sf_dst sf_size sf_start sf_end sf_tcp sf_sink sf_ftp

	set fid $sf_fid($i)
	set src $sf_src($i)
	set dst $sf_dst($i)
	set size $sf_size($i)
	set start $sf_start($i)
	set end $sf_end($i)
	set tcp $sf_tcp($i)
	set sink $sf_sink($i)
	set ftp $sf_ftp($i)

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
    #Agent/TCP set dctcp_ false
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
#query flow: 2-20KB
#qf_
#short (message) flow: 20KB-1MB
#sf_
#large flow: 1MB-100MB
#lf_

#server group: sg
set sg 1
#server count sc
set sc 4

#flow count fc
set fc 0

#time unit: second
set t_unit 0.001

#short flow start_time
set sf_start_off 0.005

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
		$ns simplex-link $rack($i) $server($i,$j) 1000Mb .002ms RED
		$ns simplex-link $server($i,$j) $rack($i) 1000Mb .002ms DropTail
		$ns queue-limit $rack($i) $server($i,$j) $queue_limit
		$ns queue-limit $server($i,$j) $rack($i) 1000
		$ns duplex-link-op $server($i,$j) $rack($i) queuePos 0.5
	}
}

#short (message) flow: update control state on the workers 100KB-1MB

#set short (message) flow id
for {set i 0} {$i < $sfc} {incr i 1} {
	set sf_fid($i) $fc
	incr fc 1
}
#set flow's src & dst
set r1 [udr 0 $sg]
set r2 [udr 0 $sc]
for {set i 0} {$i < $sfc} {incr i 1} {
	set src "[expr int([$r1 value])],[expr int([$r2 value])]"
	set dst "[expr int([$r1 value])],[expr int([$r2 value])]"
	while {$src == $dst} {
		set dst "[expr int([$r1 value])],[expr int([$r2 value])]"
	}
	#puts "short flow $i, src: $src, dst:$dst"
	set sf_src($i) $server($src)
	set sf_dst($i) $server($dst)

}

#
#set short (message) flow's size
#
set r3 [udr 20 1001]
for {set i 0} {$i < $sfc} {incr i 1} {
	set sf_size($i) [expr int([expr [$r3 value]*1000])]
	#puts "flow $i, flow size: [expr $sf_size($i)]"
}
#
#set flow's start & end time
#
#time count = 0.1s/t_unit = 100
set t_count [expr int(0.1/$t_unit)]
set avg [expr $sfc*1.0/$t_count]
#puts "avg = $avg"
set shape 5
set r4 [prr $avg $shape]
#count of short flows that has start time
set t_sfc 0
set t_start_time [expr $sf_start_off + 0.0]
for {set i 0} {$i < 100} {incr i 1} {
	#t_sfc: count of short flows that start at time $t_unit*$i
	set t1_sfc $t_sfc
	set t2_sfc [expr int([$r4 value] + 0.5)]
	#puts "pareto random = $t2_sfc"
	set t_sfc [expr $t1_sfc + $t2_sfc]
	for {set j $t1_sfc} {$j < $t_sfc} {incr j 1} {
		set t_start($j) $t_start_time
	}
	set t_start_time [expr $t_start_time + $t_unit]
}
for {set i 0} {$i < $sfc} {incr i 1} {
	set sf_start($i) -1
	set sf_end($i) -1
	if {$i < $t_sfc} {
		set sf_start($i) $t_start($i)
	}
}
puts "short flow count = $t_sfc"
#
#set flow's Transmission Layer
#
for {set i 0} {$i < $sfc} {incr i 1} {
	set sf_tcp($i) [new Agent/TCP/FullTcp/Sack]
	set sf_sink($i) [new Agent/TCP/FullTcp/Sack]
	$sf_sink($i) listen
}


#
#set flow's Application Layer
#
for {set i 0} {$i < $sfc} {incr i 1} {
	set sf_ftp($i) [new Application/FTP]
}

for {set i 0} {$i < $sfc} {incr i 1} {
	#puts "short flow $i start at $sf_start($i)"
	start_flow $i 
}

#large flow: copy fresh data to workers 1MB-100MB

$ns at 10.0 "finish"

$ns run
