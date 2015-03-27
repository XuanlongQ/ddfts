proc my_trace { } {
    global ns sc sg trace_sampling_interval queue_monitor queue_file
    
    set now [$ns now]
    for {set i 0} {$i < $sg} {incr i 1} {
	    for {set j 0} {$j < $sc} {incr j 1} {
            $queue_monitor($i,$j) instvar parrivals_ pdepartures_ pdrops_ bdepartures_ size_
            #now $rack $server $queue_size_
            puts $queue_file "$now $i $j $size_"    
            $ns at [expr $now + $trace_sampling_interval] "my_trace"

        }
    }
    
}
