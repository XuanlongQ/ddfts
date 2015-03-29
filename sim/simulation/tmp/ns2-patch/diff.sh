#!/bin/sh
if [ "$1"x = ""x ]; then
ORIGIN=""
elif [ "$1"x = "."x ]; then
ORIGIN=""
else
ORIGIN="$1-"
fi

if [ "$2"x = x ]; then
MODIFY="dctcp"
else
MODIFY=$2
fi
echo "diff -crbB ${ORIGIN}ns-default.tcl $MODIFY-ns-default.tcl"
diff -crbB "$ORIGIN"ns-default.tcl $MODIFY-ns-default.tcl
echo "@@@l@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "diff -crbB ${ORIGIN}red.cc $MODIFY-red.cc"
diff -crbB "$ORIGIN"red.cc $MODIFY-red.cc
echo "@@@l@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "diff -crbB ${ORIGIN}tcp.cc $MODIFY-tcp.cc"
diff -crbB "$ORIGIN"tcp.cc $MODIFY-tcp.cc
echo "@@@l@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "diff -crbB ${ORIGIN}tcp.h $MODIFY-tcp.h"
diff -crbB "$ORIGIN"tcp.h $MODIFY-tcp.h
echo "@@@l@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "diff -crbB ${ORIGIN}tcp-full.cc $MODIFY-tcp-full.cc"
diff -crbB "$ORIGIN"tcp-full.cc $MODIFY-tcp-full.cc
echo "@@@l@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "diff -crbB ${ORIGIN}tcp-full.h $MODIFY-tcp-full.h"
diff -crbB "$ORIGIN"tcp-full.h $MODIFY-tcp-full.h
