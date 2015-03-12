1. simulation query traffic and background flow in simulation.tcl
2. model simulation, flow
    1.1 simulation[sid, RTT, queue_limit, dctcp, topo,]
    1.2 flow[fid, ftype start, end, src, dst, pkg_size, size, drop_count,]
        ftype: query traffic(0), background flow{short message(1), large/throughtput-sensitive(2)}
3. classify flows according flow size
4. plot:
        4.1 plot CDF of time between arrivals of new work for the Aggregator(queries)
        4.2 plot CDF of time between arrivals of new background flows
        4.3 plot PDF of flow size for background flow: count of flow{f_size between (s1,s2]}/count of all flow
        4.4 plot PDF of byte for background flow: sum of bytes of flow{f_size between (s1,s2]}/sum of bytes of all flow
