[S] Solved
[C] to be Continue
. simulation query traffic and background flow in simulation.tcl
    [s] framework setup
    [c] unit test, parament reconfiguration
. awk out.tr: flow delay, flow packet-drop, total throughtput
. model simulation, flow
    1 simulation[sid, dctcp,]
    2 flow[fid, ftype start, end, deadline, src, dst, size, drcount, thrput, finished]
        ftype: query traffic(0), background flow{short message(1), large/throughtput-sensitive(2)}
        drcount: dropped packet count
. classify flows according flow size
. plot:
        1. plot CDF of time between arrivals of new work for the Aggregator(queries)
        2. plot CDF of time between arrivals of new background flows
        3. plot PDF of flow size for background flow: count of flow{f_size between (s1,s2]}/count of all flow
        4. plot PDF of byte for background flow: sum of bytes of flow{f_size between (s1,s2]}/sum of bytes of all flow
