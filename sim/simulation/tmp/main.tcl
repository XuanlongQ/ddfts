# Creating New Simulator
set ns [new Simulator]

set packetSize 1460
Agent/TCP set packetSize_ $packetSize

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
	puts "Simulation completed."
	close $nf
	close $f
	#exec nam out.nam &
	exit 0
}


#server group: sg
set sg 1
#server number sn
set sn 4

set color 0

for {set i 0} {$i < $sg} {incr i 1} {
	#
	#Create Nodes
	#
	set rack($i) [$ns node]
      		puts "rack([expr $i]): [$rack($i) id]"
	for {set j 0} {$j < $sn} {incr j 1} {
		set server($i,$j) [$ns node]
      			puts "server([expr $i],[expr $j]): [$server($i,$j) id]"
		$ns duplex-link $rack($i) $server($i,$j) 10Mb .9ms DropTail
		$ns queue-limit $rack($i) $server($i,$j) 10
		$ns duplex-link-op $server($i,$j) $rack($i) queuePos 0.5
	}
}


#query flow: 2KB-20KB

#short message flow: update control state on the workers 100KB-1MB
#
for {set i 0} {$i < $sg} {incr i 1} {
	for {set j 0} {$j < $sn} {incr j 1} {
		for {set k 0} {$k < $sn} {incr k 1} {
			
			if {$k == $j} {
				continue
			}

			set mf_tcp($i,$j,$k) [new Agent/TCP]
			$ns attach-agent $server($i,$j) $mf_tcp($i,$j,$k)
			set mf_sink($i,$j,$k) [new Agent/TCPSink]
			$ns attach-agent $server($i,$k) $mf_sink($i,$j,$k)
			$ns connect $mf_tcp($i,$j,$k) $mf_sink($i,$j,$k)
			$mf_tcp($i,$j,$k) set fid_ $color
			incr color 1

			#ftp
			set mf_ftp($i,$j,$k) [new Application/FTP]
			$mf_ftp($i,$j,$k) attach-agent $mf_tcp($i,$j,$k)
			$mf_ftp($i,$j,$k) set type_ FTP
		}
	}
}



#large flow: copy fresh data to workers 1MB-100MB
#
for {set i 0} {$i < $sg} {incr i 1} {
	for {set j 0} {$j < $sn} {incr j 1} {

		set lf_tcp($i,$j) [new Agent/TCP]
		$ns attach-agent $server($i,$j) $lf_tcp($i,$j)
		set lf_sink($i,$j) [new Agent/TCPSink]
		set jj [expr ($j + 1) % $sn]
		$ns attach-agent $server($i,$jj) $lf_sink($i,$j)
		$ns connect $lf_tcp($i,$j) $lf_sink($i,$j)
		$lf_tcp($i,$j) set fid_ $color
		incr color 1

		#ftp
		set lf_ftp($i,$j) [new Application/FTP]
		$lf_ftp($i,$j) attach-agent $lf_tcp($i,$j)
		$lf_ftp($i,$j) set type_ FTP
	}
}


#
#Start up the sources
#
#query flow
for {set i 0} {$i < $sg} {incr i 1} {
	for {set j 0} {$j < $sn} {incr j 1} {
		#$ns at 0.1 "$lf_ftp([expr $i],[expr $j]) start"
		#$ns at 4.9 "$lf_ftp([expr $i],[expr $j]) stop"
	}
}

#message flow
set count 0
for {set i 0} {$i < $sg} {incr i 1} {
	for {set j 0} {$j < $sn} {incr j 1} {
		for {set k 0} {$k < $sn} {incr k 1} {
			if {$k == $j} {
				continue
			}
			#$ns at [expr 0.1 + 0.09 * $count] "$mf_ftp([expr $i],[expr $j],[expr $k]) send 50000"
		}
		incr count 1
	}
}
$ns at 0.001 "$mf_ftp(0,0,1) send 1600"

#large flow
for {set i 0} {$i < $sg} {incr i 1} {
	for {set j 0} {$j < $sn} {incr j 1} {
		#$ns at 0.0 "$lf_ftp([expr $i],[expr $j]) start"
		#$ns at 3.0 "$lf_ftp([expr $i],[expr $j]) stop"
	}
}
$ns at 10.0 "finish"

$ns run
