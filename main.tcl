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
	puts "Simulation completed."
	close $nf
	close $f
	exec nam out.nam &
	exit 0
}


#
#Create Nodes
#

set rack1 [$ns node]
      puts "rack1: [$rack1 id]"
set s1 [$ns node]
      puts "s1: [$s1 id]"
set s2 [$ns node]
      puts "s2: [$s2 id]"
set s3 [$ns node]
      puts "s3: [$s3 id]"
set s4 [$ns node]
      puts "s4: [$s4 id]"


#
#Setup Connections
#

$ns duplex-link $s2 $rack1 1000Mb 2ms DropTail

$ns duplex-link $s3 $rack1 1000Mb 2ms DropTail

$ns duplex-link $s4 $rack1 1000Mb 2ms DropTail

$ns duplex-link $rack1 $s1 1000Mb 2ms DropTail



#
#Set up Transportation Level Connections
#

#s1
set sink5 [new Agent/TCPSink]
$ns attach-agent $s1 $sink5

set sink6 [new Agent/TCPSink]
$ns attach-agent $s1 $sink6

set sink7 [new Agent/TCPSink]
$ns attach-agent $s1 $sink7

set sink10 [new Agent/TCPSink]
$ns attach-agent $s1 $sink10

set sink8 [new Agent/TCPSink]
$ns attach-agent $s1 $sink8

set s1_s2_ftp1_sink [new Agent/TCPSink]
$ns attach-agent $s1 $s1_s2_ftp1_sink

#s2
set s2_prt_tcp [new Agent/TCP/Reno]
$ns attach-agent $s2 $s2_prt_tcp

set s2_ftp_tcp [new Agent/TCP/Reno]
$ns attach-agent $s2 $s2_ftp_tcp

#s3
set s3_prt_tcp [new Agent/TCP/Reno]
$ns attach-agent $s3 $s3_prt_tcp

set s3_ftp_tcp [new Agent/TCP/Reno]
$ns attach-agent $s3 $s3_ftp_tcp

#s4
set s4_ftp_tcp [new Agent/TCP/Reno]
$ns attach-agent $s4 $s4_ftp_tcp

set s4_prt_tcp [new Agent/TCP/Reno]
$ns attach-agent $s4 $s4_prt_tcp



#
#Setup traffic sources
#

#pareto

#s2
set s2_prt1 [new Application/Traffic/Pareto]
    $s2_prt1 set packetSize_ 500
$s2_prt1 attach-agent $s2_prt_tcp

set s2_prt2 [new Application/Traffic/Pareto]
    $s2_prt2 set packetSize_ 500
$s2_prt2 attach-agent $s2_prt_tcp

#s3
set s3_prt1 [new Application/Traffic/Pareto]
    $s3_prt1 set packetSize_ 500
$s3_prt1 attach-agent $s3_prt_tcp

set s3_prt2 [new Application/Traffic/Pareto]
    $s3_prt2 set packetSize_ 500
$s3_prt2 attach-agent $s3_prt_tcp

#s4
set s4_prt1 [new Application/Traffic/Pareto]
    $s4_prt1 set packetSize_ 500
$s4_prt1 attach-agent $s4_prt_tcp

set s4_prt2 [new Application/Traffic/Pareto]
    $s4_prt2 set packetSize_ 500
$s4_prt2 attach-agent $s4_prt_tcp

#ftp

#s2
set ftp0 [new Application/FTP]
$ftp0 attach-agent $s2_ftp_tcp

#s3
set ftp1 [new Application/FTP]
$ftp1 attach-agent $s3_ftp_tcp

#s4
set ftp2 [new Application/FTP]
$ftp2 attach-agent $s4_ftp_tcp

$ns connect $s2_ftp_tcp $s1_s2_ftp1_sink
$s2_ftp_tcp set fid_ 0
$ns connect $s4_ftp_tcp $sink6
$s4_ftp_tcp set fid_ 2
$ns connect $s3_ftp_tcp $sink5
$s3_ftp_tcp set fid_ 1
$ns connect $s2_prt_tcp $sink7
$s2_prt_tcp set fid_ 3
$ns connect $s3_prt_tcp $sink8
$s3_prt_tcp set fid_ 4
$ns connect $s4_prt_tcp $sink10
$s4_prt_tcp set fid_ 5

#
#Start up the sources
#

$ns at 0.1 "$ftp0 start"
$ns at 5 "$ftp0 stop"
$ns at 0.2 "$ftp1 start"
$ns at 5.1 "$ftp1 stop"
$ns at 0.3 "$ftp2 start"
$ns at 5.2 "$ftp2 stop"
$ns at 5.5 "$s2_prt1 start"
$ns at 5.6 "$s2_prt2 start"
$ns at 5.7 "$s3_prt1 start"
$ns at 5.8 "$s3_prt2 start"
$ns at 5.9 "$s4_prt1 start"
$ns at 6 "$s4_prt2 start"
$ns at 10 "$s2_prt1 stop"
$ns at 10.3 "$s2_prt2 stop"
$ns at 10.6 "$s3_prt1 stop"
$ns at 10.9 "$s3_prt2 stop"
$ns at 11.2 "$s4_prt1 stop"
$ns at 11.5 "$s4_prt2 stop"
$ns at 12.0 "finish"
$ns run
