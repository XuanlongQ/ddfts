#!/bin/sh
echo "diff -crbB ns-default.tcl dctcp-ns-default.tcl"
diff -crbB ns-default.tcl dctcp-ns-default.tcl
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "diff -crbB red.cc dctcp-red.cc"
diff -crbB red.cc dctcp-red.cc
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "diff -crbB tcp.cc dctcp-tcp.cc"
diff -crbB tcp.cc dctcp-tcp.cc
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "diff -crbB tcp.h dctcp-tcp.h"
diff -crbB tcp.h dctcp-tcp.h
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "diff -crbB tcp-full.cc dctcp-tcp-full.cc"
diff -crbB tcp-full.cc dctcp-tcp-full.cc
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "diff -crbB tcp-full.h dctcp-tcp-full.h"
diff -crbB tcp-full.h dctcp-tcp-full.h
