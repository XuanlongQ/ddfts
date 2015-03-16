#query flow: 1.6-2KB
proc setup_query_flow {} {
        global ftpPkgSize
        global sg sc server
        global qfc fc
        global qf_fid qf_src qf_dst qf_size qf_start qf_end
        global qf_tcp qf_sink qf_ftp
        global udr prr
        global sim_end_time
        #1. use $prr to generate query flow arrival time list
        #qat_list[]
        #set avg according CDF of time between background flows(@DCTCP)
        set avg 0.1
        set shape 5
        set r [prr $avg $shape]
        set qat_list(0) 0.03
        set i 0
        while { $qat_list($i) < $sim_end_time } {
            set ii $i
            incr i
            set qat_list($i) [expr [$r value] + $qat_list($ii)]
        }
        set qfc [expr $i]
        if { $qat_list($i) < $sim_end_time } {
            incr qfc
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
        for {set i 0} {$i < $qfc} {incr i 1} {
            set src "[expr int([$r1 value])],[expr int([$r2 value])]"
            set dst "[expr int([$r1 value])],[expr int([$r2 value])]"
            while {$src == $dst} {
                set dst "[expr int([$r1 value])],[expr int([$r2 value])]"
            }
            #puts "short flow $i, src: $src, dst:$dst"
            set qf_src($i) $src
            set qf_dst($i) $dst

        }

        #
        #set short (message) flow's size
        #
        set r3 [udr 1.6 2]
        for {set i 0} {$i < $qfc} {incr i 1} {
            set qf_size($i) [expr int([expr [$r3 value]*$ftpPkgSize])]
            #puts "flow $i, flow size: [expr $qf_size($i)]"
        }
        #
        #set flow's start //& end time
        #
        for {set i 0} {$i < $qfc} {incr i 1} {
            set qf_start($i) $qat_list($i)
        }
        #
        #set flow's Transmission Layer
        #
        for {set i 0} {$i < $qfc} {incr i 1} {
            set qf_tcp($i) [new Agent/TCP/FullTcp/Sack]
            set qf_sink($i) [new Agent/TCP/FullTcp/Sack]
            $qf_sink($i) listen
        }


        #
        #set flow's Application Layer
        #
        for {set i 0} {$i < $qfc} {incr i 1} {
            set qf_ftp($i) [new Application/FTP]
        }

        for {set i 0} {$i < $qfc} {incr i 1} {
            #puts "query flow $i start at $qf_start($i)"
            puts "flow:$qf_fid($i)|ftype:q|deadline:-1|src:$qf_src($i)|dst:$qf_dst($i)|size:$qf_size($i)"
            start_flow $i q
        }
}
