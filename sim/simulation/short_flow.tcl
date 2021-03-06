#short (message) flow: update control state on the workers 100KB-1MB
proc setup_short_flow {} {
        global ns
        global flow_file
        #flow count fc
        global fc
        #short (message) flow count
        global sfc
        global sf_fid sf_src sf_dst sf_size sf_start sf_end
        global sg sc server
        global udr prr
        global sf_tcp sf_sink sf_ftp
        global sim_end_time
        #1. use $prr to generate short flow arrival time list
        #sat_list[]
        #set avg according CDF of time between background flows(@DCTCP)
        set avg 0.2
        set shape 25
        set r [prr $avg $shape]
        set sat_list(0) 0.02
        set i 0
        while { $sat_list($i) < $sim_end_time } {
            set ii $i
            incr i
            set sat_list($i) [expr [$r value] + $sat_list($ii)]
        }
        set sfc [expr $i]
        if { $sat_list($i) < $sim_end_time } {
            incr sfc
        }
        puts "short flow count: = $sfc"
        puts $flow_file "sfc:$sfc"

        #set short (message) flow id
        for {set i 0} {$i < $sfc} {incr i 1} {
            set sf_fid($i) $fc
            incr fc 1
        }
        #set flow's src & dst
        set r1 [udr 0 $sg]
        set r2 [udr 0 $sc]
        for {set i 0} {$i < $sfc} {incr i 1} {
            set src "[expr int([$r1 value])],[expr int([$r2 value])]"
            set dst "[expr int([$r1 value])],[expr int([$r2 value])]"
            while {$src == $dst} {
                set dst "[expr int([$r1 value])],[expr int([$r2 value])]"
            }
            #puts "short flow $i, src: $src, dst:$dst"
            set sf_src($i) $src
            set sf_dst($i) $dst

        }

        #
        #set short (message) flow's size
        #
        set r3 [udr 2 1001]
        for {set i 0} {$i < $sfc} {incr i 1} {
            set sf_size($i) [expr int([$r3 value])*1000]
            #puts "flow $i, flow size: [expr $sf_size($i)]"
        }
        #
        #set flow's start //& end time
        #
        for {set i 0} {$i < $sfc} {incr i 1} {
            set sf_start($i) $sat_list($i)
        }
        #
        #set flow's Transmission Layer
        #
        for {set i 0} {$i < $sfc} {incr i 1} {
            set sf_tcp($i) [new Agent/TCP/FullTcp/Sack]
            set sf_sink($i) [new Agent/TCP/FullTcp/Sack]
	        $ns attach-agent $server($sf_src($i)) $sf_tcp($i)
	        $ns attach-agent $server($sf_dst($i)) $sf_sink($i)
	        $ns connect $sf_tcp($i) $sf_sink($i)
	        $sf_tcp($i) set fid_ $sf_fid($i)
            $sf_sink($i) listen
        }


        #
        #set flow's Application Layer
        #
        for {set i 0} {$i < $sfc} {incr i 1} {
            set sf_ftp($i) [new Application/FTP]
	        $sf_ftp($i) attach-agent $sf_tcp($i)
	        $sf_ftp($i) set type_ FTP
        }

        for {set i 0} {$i < $sfc} {incr i 1} {
            #puts "short flow $i start at $sf_start($i)"
            puts $flow_file "flow:$sf_fid($i)|ftype:s|deadline:-1|src:$sf_src($i)|dst:$sf_dst($i)|size:$sf_size($i)"
		    $ns at $sf_start($i) "$sf_ftp($i) send $sf_size($i)"
        }
}
