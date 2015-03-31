proc my_trace { } {

    global ns sc sg trace_sampling_interval queue_monitor queue_file
    set now [$ns now]
    set now_ [expr int([expr $now*1000000])]
    for {set i 0} {$i < $sg} {incr i 1} {
	    for {set j 0} {$j < $sc} {incr j 1} {
            $queue_monitor($i,$j) instvar parrivals_ pdepartures_ pdrops_ bdepartures_ pkts_ size_
            #now $rack $server $queue_size_
            puts $queue_file "$now_ $i $j $pkts_ $size_"    
        }
    }
    $ns at [expr $now + $trace_sampling_interval] "my_trace"
}

proc tcp_trace {tcp} {

    global ns trace_sampling_interval tcp_file
    set now [$ns now]
	set cwnd [$tcp set cwnd_]
	set dctcp_alpha [$tcp set dctcp_alpha_]
	set d2tcp_dline [$tcp set d2tcp_d_]
    #now cwnd0 cwnd1 ... cwnd$N
    #now alpha0 alpha1 ... alpha$N
    puts -nonewline $tcp_file [format "%.4lf %.2lf" $now $cwnd]
    puts $tcp_file [format " %.3lf^%.3lf" $dctcp_alpha $d2tcp_dline]

    $ns at [expr $now + $trace_sampling_interval] "tcp_trace $tcp"
}
