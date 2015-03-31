[S] Solved
[C] to be Continue

.[S] simulation query traffic and background flow in simulation.tcl
     framework setup
.[S] analyse flow out.tr: flow delay, flow packet-drop, flow throughtput
    [S] using python script to replace awk script
.[S] model simulation, flow
    1. simulation[sid, dctcp, qfcnt, sfcnt, lfcnt, afcnt, status]
            dctcp: enable or disable dctcp
            qft: query flow count
            sft: short flow count
            lft: large flow count
            aft: all flow count
            status: 0-> undone, 1->processing, 2->done
    2. flow[fid, ftype start, end, deadline, src, dst, size, drcnt, thrput, finished, sim]
            ftype: query traffic(0), background flow{short message(1), large/throughtput-sensitive(2)}
            drcnt: dropped packet count
            sim: simulation which flow belongs to
.[S] sim/simtool.py: call simulation.tcl to simulate network
     get full flow info after simulation and save to db
.[S] plot:
        1. plot CDF of time between arrivals of new work for the Aggregator(queries)
        2. plot CDF of time between arrivals of new background flows
        3. plot PDF of background flow count : count of flow{f_size between (s1,s2]}/count of all flow
        4. plot PDF of background flow byte: sum of bytes of flow{f_size between (s1,s2]}/sum of bytes of all flow

[S]. reconfigure query traffic pattern using TcpApp
[S]. add delay for resonese of query flow
[S]. remodel simulation, flow
    1. simulation[sid, dctcp, qfcnt, sfcnt, lfcnt, afcnt, status, time]
    2. flow[fid, ftype start, end, deadline, src, dst, size, {pktcnt}, drcnt, thrput, finished, sim]
        finished = (thrput >= size + 40*pktcnt)
[S]. in sim home page, add function to create a simulation
[S]. add simthread which regularly gets undone simulation from db and make it
[S]. filter flow that has finished transportation in analyse_flow.py by comparing flow size and throughput //or by FYN packet
[S]. create head navigate template for sim app
[S]. trace queue length
[S]. remodel simulation
    simulation[sid, {tcptype}, qfcnt, sfcnt, lfcnt, afcnt, status, time]
        tcptype: tcp, dctcp, d2tcp
[S]. proving the difference of tcp, dctcp, d2tcp using cwnd & alpha tracer
[S]. model qrecord[qid, time, rack, server, pktcnt, size, sim]
[S]. plot PDF of queue length by time
. reconfigure query traffic arrival time according to plotted png
. reconfigure background traffic arrival time according to plotted png
. adjust PDF of background flow count/byte x axis: 10^3, 10^4, 10^5, 10^6, 10^7, 10^8
