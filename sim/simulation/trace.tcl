proc my_trace { } {
    global ns sc sg trace_sampling_interval queue_monitor queue_file
    
    set now [$ns now]
    for {set i 0} {$i < $sg} {incr i 1} {
	    for {set j 0} {$j < $sc} {incr j 1} {
            $queue_monitor($i,$j) instvar parrivals_ pdepartures_ pdrops_ bdepartures_ pkts_ size_
            #now $rack $server $queue_size_
            puts $queue_file "$now $i $j $pkts_ $size_"    
        }
    }
    
    if { 0 } { 
    set N 0
    for {set i 0} {$i < $sg} {incr i 1} {
	    for {set j 0} {$j < $sc} {incr j 1} {
	        set cwnd($i) [$tcp($i) set cwnd_]
	        set dctcp_alpha($i) [$tcp($i) set dctcp_alpha_]
	        set d2tcp_dline($i) [$tcp($i) set d2tcp_d_]
        }
    }
    #now cwnd0 cwnd1 ... cwnd$N
    #now alpha0 alpha1 ... alpha$N
    puts -nonewline $cwnd_file [format "%.4lf %.2lf" $now $cwnd(0)]
    for {set i 1} {$i < $N} {incr i} {
	    puts -nonewline $cwnd_file [format " %.2lf" $cwnd($i)]
    }
    puts $cwnd_file ""    

    puts -nonewline $alpha_file [format "%.4lf %.3lf^%.3lf" $now $dctcp_alpha(0) $d2tcp_dline(0)]
    for {set i 0} {$i < $N} {incr i} {
	    puts -nonewline $alpha_file [format " %.3lf^%.3lf" $dctcp_alpha($i) $d2tcp_dline($i)]
    }
    puts $alpha_file ""    


    $ns at [expr $now + $trace_sampling_interval] "my_trace"
    }
    
}
