#query flow: 1.6-2KB
proc setup_query_flow {} {
        global ns
        global ftpPkgSize
        global sg sc server
        global qfc fc
        global qf_fid qf_src qf_dst qf_size qf_start qf_end
        global qf_tcp qf_sink qf_ftp qf_sftp
        global udr prr
        global sim_end_time
        #1. use $prr to generate query flow arrival time list
        #qat_list[]
        #set avg according CDF of time between background flows(@DCTCP)
        #avg = 500 ms
        set avg 0.5
        set shape 5.5
        set r [prr $avg $shape]
        #set avg 0.4
        #set r [epr $avg]
        #set r [udr 0 0.6]
        set qat_list(0) 0.03
        set i 0
        while { $qat_list($i) < $sim_end_time } {
            set ii $i
            incr i
            set qat_list($i) [expr [$r value] + $qat_list($ii)]
        }
        #each of HLA queries(i) split into ($sc-1) MLA queries
        set qfc [expr $i*($sc-1)]
        if { $qat_list($i) < $sim_end_time } {
            incr qfc [expr $sc-1]
        }
        puts "query flow count: = $qfc"
        puts "qfc:$qfc"
        
        #set query flow id
        for {set i 0} {$i < $qfc} {incr i 1} {
            set qf_fid($i) $fc
            incr fc 1
        }
        #set flow's src & dst
        set r1 [udr 0 $sg]
        set r2 [udr 0 $sc]
        for {set i 0} {$i < $qfc} { } {
            set tg [expr int([$r1 value])]
            set ts [expr int([$r2 value])]
            set src "$tg,$ts"
            for {set j 0} {$j < $sc} {incr j 1} {
                if {$j == $ts} {
                    continue
                }
                set dst "$tg,$j"
                #puts "short flow $i, src: $src, dst:$dst"
                set qf_src($i) $src
                set qf_dst($i) $dst
                incr i
            }

        }

        #
        #set query flow's size
        #
        set r3 [udr 1.6 2]
        for {set i 0} {$i < $qfc} {incr i 1} {
            set qf_size($i) [expr int([expr [$r3 value]*$ftpPkgSize])]
            #puts "flow $i, flow size: [expr $qf_size($i)]"
        }
        #
        #set flow's start //& end time
        #
        for {set i 0} {$i < $qfc} {incr i} {
            set qf_start($i) $qat_list([expr $i/($sc-1)])
        }
        #
        #set flow's Transmission Layer
        #
        for {set i 0} {$i < $qfc} {incr i 1} {
            set qf_tcp($i) [new Agent/TCP/FullTcp/Sack]
            set qf_sink($i) [new Agent/TCP/FullTcp/Sack]
            $ns attach-agent $server($qf_src($i)) $qf_tcp($i)
            $ns attach-agent $server($qf_dst($i)) $qf_sink($i)
            $ns connect $qf_tcp($i) $qf_sink($i)
            $qf_tcp($i) set fid_ $qf_fid($i)
            $qf_sink($i) set fid_ $qf_fid($i)
            $qf_sink($i) listen
        }


        #
        #set flow's Application Layer
        #
        for {set i 0} {$i < $qfc} {incr i 1} {
            set qf_ftp($i) [new Application/TcpApp $qf_tcp($i)]
            set qf_sftp($i) [new Application/TcpApp $qf_sink($i)]
            $qf_ftp($i) connect $qf_sftp($i)
        }

        for {set i 0} {$i < $qfc} {incr i 1} {
            if { $qf_start($i) > 0 && $qf_size($i) > 0} {
                #puts "query flow $i start at $qf_start($i)"
                puts "flow:$qf_fid($i)|ftype:q|deadline:-1|src:$qf_src($i)|dst:$qf_dst($i)|size:$qf_size($i)"
                set sftp $qf_sftp($i)
                $ns at $qf_start($i) "$qf_ftp($i) send $qf_size($i) {$sftp recv {$i}}"
                #puts "$t flow $i\[[$src id]->[$dst id]\] start at $start and the size is [expr $size*1.0/$ftpPkgSize]"
            }
        }
}


#response delay for query traffic
set rr_avg 0.05
set rr_shape 5
set rr [prr $rr_avg $rr_shape]
Application/TcpApp instproc recv {i} {
	global ns qf_sftp qf_ftp qf_start rr
    if { $i>0 } {
        $ns at [expr [$ns now] + [$rr value]] "$qf_sftp($i) send 2000 {$qf_ftp($i) recv {-1}}"
    }
}
