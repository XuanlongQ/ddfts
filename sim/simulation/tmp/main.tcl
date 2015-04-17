# Creating New Simulator
set ns [new Simulator]

set packetSize 1460
Agent/TCP set packetSize_ $packetSize

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

set s [$ns node]
set r [$ns node]

$ns duplex-link $s $r 1000Mb .2ms DropTail

set tcp [new Agent/TCP]
set sink [new Agent/TCPSink]

$ns attach-agent $s $tcp
$ns attach-agent $r $sink
$ns connect $tcp $sink

set ftp [new Application/FTP]
$ftp attach-agent $tcp

$ns at 0.00 "$ftp send 3470"

$ns at 10.0 "finish"

$ns run
