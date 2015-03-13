#large flow: copy fresh data to workers 1MB-100MB
proc setup_large_flow {} {
        global lfc fc
        global lf_fid lf_src lf_dst lf_size lf_start lf_end
        global sg sc server
        global udr prr
        global lf_tcp lf_sink lf_ftp
        global sim_end_time
        #1. use $prr to generate large flow arrival time list
        #lat_list[]
        #set avg according CDF of time between background flows(@DCTCP)
        set avg 0.5
        set shape 5
        set r [prr $avg $shape]
        set lat_list(0) 0.01
        set i 0
        while { $lat_list($i) < $sim_end_time } {
            set ii $i
            incr i
            set lat_list($i) [expr [$r value] + $lat_list($ii)]
        }
        set lfc [expr $i+1]
        #puts "lfc=$lfc"

        #set large flow id
        for {set i 0} {$i < $lfc} {incr i 1} {
            set lf_fid($i) $fc
            incr fc 1
        }
        #set flow's src & dst
        set r1 [udr 0 $sg]
        set r2 [udr 0 $sc]
        for {set i 0} {$i < $lfc} {incr i 1} {
            set src "[expr int([$r1 value])],[expr int([$r2 value])]"
            set dst "[expr int([$r1 value])],[expr int([$r2 value])]"
            while {$src == $dst} {
                set dst "[expr int([$r1 value])],[expr int([$r2 value])]"
            }
            #puts "large flow $i, src: $src, dst:$dst"
            set lf_src($i) $server($src)
            set lf_dst($i) $server($dst)

        }

        #
        #set large flow's size
        #
        set r3 [udr 20 1001]
        for {set i 0} {$i < $lfc} {incr i 1} {
            set lf_size($i) [expr int([expr [$r3 value]*1000])]
            #puts "flow $i, flow size: [expr $lf_size($i)]"
        }
        #
        #set flow's start //& end time
        #
        for {set i 0} {$i < $lfc} {incr i 1} {
            set lf_start($i) $lat_list($i)
        }
        #
        #set flow's Transmission Layer
        #
        for {set i 0} {$i < $lfc} {incr i 1} {
            set lf_tcp($i) [new Agent/TCP/FullTcp/Sack]
            set lf_sink($i) [new Agent/TCP/FullTcp/Sack]
            $lf_sink($i) listen
        }


        #
        #set flow's Application Layer
        #
        for {set i 0} {$i < $lfc} {incr i 1} {
            set lf_ftp($i) [new Application/FTP]
        }

        for {set i 0} {$i < $lfc} {incr i 1} {
            puts "large flow $i start at $lf_start($i)"
            start_flow $i l
        }
}
