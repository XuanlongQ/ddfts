#flow id: i, flow_type: t
proc start_flow {i t} {

	global ns
    global server
    global ftpPkgSize
    global ${t}f_fid
    global ${t}f_src ${t}f_dst ${t}f_size
    global ${t}f_start ${t}f_end
    global ${t}f_tcp ${t}f_sink ${t}f_ftp

	eval "set fid \$${t}f_fid($i)"
	eval "set src \$server(\$${t}f_src($i))"
	eval "set dst \$server(\$${t}f_dst($i))"
	eval "set size \$${t}f_size($i)"
	eval "set start \$${t}f_start($i)"
	eval "set tcp \$${t}f_tcp($i)"
	eval "set sink \$${t}f_sink($i)"
	eval "set ftp \$${t}f_ftp($i)"

	$ns attach-agent $src $tcp
	$ns attach-agent $dst $sink
	$ns connect $tcp $sink
	$tcp set fid_ $fid

	#ftp
	$ftp attach-agent $tcp
	$ftp set type_ FTP
	
	if { $start > 0 && $size > 0} {
		$ns at $start "$ftp send $size"
		#puts "$t flow $i\[[$src id]->[$dst id]\] start at $start and the size is [expr $size*1.0/$ftpPkgSize]"
	}
}
