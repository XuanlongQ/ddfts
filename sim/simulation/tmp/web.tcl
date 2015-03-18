set ns [new Simulator]

set f [open out.tr w]
$ns trace-all $f

#Create topology/routing
set node(c) [$ns node]
set node(e) [$ns node]
set node(s) [$ns node]
$ns duplex-link $node(s) $node(e) 1.5Mb 50ms DropTail
$ns duplex-link $node(e) $node(c) 10Mb 50ms DropTail
#four routing strategies in ns: Static, Session, Dynamic and Manual
#$ns rtproto Session ;# Enable sessing routing for this simulation

#HTTP logs
set log [open "http.log" w]

#Create page pool as a central page generator. Use PagePool/Math
set pgp [new PagePool/Math] ;###Page size generator
set r [new RandomVariable/Constant] ;###average page size
$r set val_ 1024
$pgp ranvar-size $r

set r [new RandomVariable/Exponential] ;##Page age generator
$r set avg_ 5 ;##average page age
$pgp ranvar-age $r

set server [new Http/Server $ns $node(s)] ;##Create a server and link it to the central page pool
$server set-page-generator $pgp
$server log $log

set cache [new Http/Cache $ns $node(e)]
$cache log $log

set client [new Http/Client $ns $node(c)]
set r [new RandomVariable/Exponential]
$r set avg_ 5
$client set-interval-generator $r
$client set-page-generator $pgp
$client log $log

set startTime 1
set finishTime 50
$ns at $startTime "start-connection"
$ns at $finishTime "finish"

proc start-connection {} {
    global ns server cache client
    $client connect $cache
    $cache connect $server
    $client start-session $cache $server
}

proc finish {} {
    global ns f log
    $ns flush-trace
    close $f
    flush $log
    close $log
    exit 0
}

$ns run
