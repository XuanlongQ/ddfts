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
		puts "flow $i\[[$src id]->[$dst id]\] start at $start and the size is $size"
	}
}
# Creating New Simulator
set ns [new Simulator]

$ns color 0 Blue
$ns color 1 Red
$ns color 2 Green
$ns color 3 Yellow
$ns color 4 Purple
$ns color 5 White

# Setting up the traces
set f [open out.tr w]
set nf [open out.nam w]
$ns namtrace-all $nf
$ns trace-all $f
proc finish {} { 
	global ns nf f
	$ns flush-trace
	#puts "Simulation completed."
	close $nf
	close $f
	exec nam out.nam &
	exit 0
}

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
		$ns duplex-link $rack($i) $server($i,$j) 1000Mb .002ms DropTail
		$ns queue-limit $rack($i) $server($i,$j) 10
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
	set sf_tcp($i) [new Agent/TCP]
	set sf_sink($i) [new Agent/TCPSink]
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

$ns at 5.0 "finish"

$ns run
