[S] Solved
[C] to be Continue
. simulation query traffic and background flow in simulation.tcl
    [S] framework setup
    [C] unit test, parament reconfiguration
. analyse flow out.tr: flow delay, flow packet-drop, flow throughtput
    [S] using python script to replace awk script
. model simulation, flow
    [S]1. simulation[sid, dctcp, done]
            dctcp: enable or disable dctcp
            done: simulation has done, flows have generated
    [S]2. flow[fid, ftype start, end, deadline, src, dst, size, drcnt, thrput, finished]
            ftype: query traffic(0), background flow{short message(1), large/throughtput-sensitive(2)}
            drcnt: dropped packet count
. sim/simtool.py: call simulation.tcl to simulate network
. classify flows according flow size
. plot:
        1. plot CDF of time between arrivals of new work for the Aggregator(queries)
        2. plot CDF of time between arrivals of new background flows
        3. plot PDF of flow size for background flow: count of flow{f_size between (s1,s2]}/count of all flow
        4. plot PDF of byte for background flow: sum of bytes of flow{f_size between (s1,s2]}/sum of bytes of all flow
