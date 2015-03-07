1.tcl script:
    INPUT:
    OUTPUT: out/$test_id/tcl

2.awk script:
    INPUT: out/$test_id/tcl
    OUTPUT: out/$test_id/awk

3.plot(python) script:
    INPUT: out/$test_id/awk
    OUTPUT:out/$test_id/plt
