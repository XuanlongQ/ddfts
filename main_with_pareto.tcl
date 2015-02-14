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
	$rng seed 0
	set r [new RandomVariable/Pareto]
	$r use-rng $rng
	$r set avg_ $avg
	$r set shape_ $shape
	return $r

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
	#exec nam out.nam &
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

#query flow count qfc
set qfc [expr 2000*$sg*$sc]
#short (message) flow count
set sfc [expr 200*$sg*$sc]
#large flow count
set lfc 100

#set src dst: uniform distribution
set r1 [udr 0 $sg]
set r2 [udr 0 $sc]
set size [udr 20 1001]
for {set i 0} {$i < $sfc} {incr i 1} {
	set src "[expr int([$r1 value])],[expr int([$r2 value])]"
	set dst "[expr int([$r1 value])],[expr int([$r2 value])]"
	while {$src == $dst} {
		set dst "[expr int([$r1 value])],[expr int([$r2 value])]"
	}
	#puts "src: $src, dst:$dst"
	set fid($fc) $fc
	set fstart($fc) -1
	set fsrc($fc) $src
	set fdst($fc) $dst
	set fsize($fc) [expr int([expr [$size value]*1000])]
	#puts "fsize: [expr $fsize($fc)]"
	set ftype($fc) "sf"
	set sf($i) $fc
	incr fc 1

}
set avg [expr $sfc/100]
	#puts "avg = $avg"
set r3 [prr $avg 5]
set t1_sfc 0
for {set i 0} {$i < 100} {incr i 1} {
	if {$t1_sfc >= $sfc} {
		puts "i === $i!!!!!!!!!!"
		break
	}
	set t2_sfc [expr int([$r3 value])]
	#puts "pareto random = $t2_sfc"
	for {set j 0} {$j < $t2_sfc} {incr j 1} {
		if {$t1_sfc >= $sfc} {
			puts "j === $j!!!!!!!!!!"
			break 
		}
		set id $sf($i)
		set fstart($id) [expr 0.1*$i]
		incr t1_sfc 1
	}
	#puts "i = $i"

}
puts "short flow count = $t1_sfc"



for {set i 0} {$i < $sg} {incr i 1} {
	#
	#Create Nodes
	#
	set rack($i) [$ns node]
      		#puts "rack([expr $i]): [$rack($i) id]"
	for {set j 0} {$j < $sc} {incr j 1} {
		set server($i,$j) [$ns node]
      			#puts "server([expr $i],[expr $j]): [$server($i,$j) id]"
		$ns duplex-link $rack($i) $server($i,$j) 10Mb .2ms DropTail
		$ns queue-limit $rack($i) $server($i,$j) 10
		$ns duplex-link-op $server($i,$j) $rack($i) queuePos 0.5
	}
}


#query flow: 2KB-20KB

#short message flow: update control state on the workers 100KB-1MB
#
for {set i 0} {$i < $sg} {incr i 1} {
	for {set j 0} {$j < $sc} {incr j 1} {
		for {set k 0} {$k < $sc} {incr k 1} {
			
			if {$k == $j} {
				continue
			}

			set mf_tcp($i,$j,$k) [new Agent/TCP]
			$ns attach-agent $server($i,$j) $mf_tcp($i,$j,$k)
			set mf_sink($i,$j,$k) [new Agent/TCPSink]
			$ns attach-agent $server($i,$k) $mf_sink($i,$j,$k)
			$ns connect $mf_tcp($i,$j,$k) $mf_sink($i,$j,$k)
			#$mf_tcp($i,$j,$k) set fid_ $color

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
	for {set j 0} {$j < $sc} {incr j 1} {

		set lf_tcp($i,$j) [new Agent/TCP]
		$ns attach-agent $server($i,$j) $lf_tcp($i,$j)
		set lf_sink($i,$j) [new Agent/TCPSink]
		set jj [expr ($j + 1) % $sc]
		$ns attach-agent $server($i,$jj) $lf_sink($i,$j)
		$ns connect $lf_tcp($i,$j) $lf_sink($i,$j)
		#$lf_tcp($i,$j) set fid_ $color

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
	for {set j 0} {$j < $sc} {incr j 1} {
		#$ns at 0.1 "$lf_ftp([expr $i],[expr $j]) start"
		#$ns at 4.9 "$lf_ftp([expr $i],[expr $j]) stop"
	}
}

#message flow
set count 0
for {set i 0} {$i < $sg} {incr i 1} {
	for {set j 0} {$j < $sc} {incr j 1} {
		for {set k 0} {$k < $sc} {incr k 1} {
			if {$k == $j} {
				continue
			}
			#$ns at [expr 0.1 + 0.09 * $count] "$mf_ftp([expr $i],[expr $j],[expr $k]) send 50000"
		}
		incr count 1
	}
}

#large flow
for {set i 0} {$i < $sg} {incr i 1} {
	for {set j 0} {$j < $sc} {incr j 1} {
		#$ns at 0.0 "$lf_ftp([expr $i],[expr $j]) start"
		#$ns at 3.0 "$lf_ftp([expr $i],[expr $j]) stop"
	}
}
$ns at 10.0 "finish"

$ns run
