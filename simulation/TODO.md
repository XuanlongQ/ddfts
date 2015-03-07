1. tcl script:
    INPUT: main.py
    OUTPUT: out/$test_id/tcl

2. awk script:
    INPUT: out/$test_id/tcl
    OUTPUT: out/$test_id/awk

3. plot(python) script:
    INPUT: out/$test_id/awk
    OUTPUT:out/$test_id/plt
###
1. simulation.tcl
    INPUT: enable_dctcp, RTT, queue_size
    OUTPUT: e.g. false_17_250.tr, false_17_250.nam 

2. measure_flow_delay.awk
    INPUT: e.g. false_17_250.tr
    OUTPUT: e.g. false_17_250_flow_delay.dat

3. plot_flow_delay.py
    INPUT: e.g. false_17_250_flow_delay.dat
    OUTPUT: e.g. false_17_250_flow_delay.png
