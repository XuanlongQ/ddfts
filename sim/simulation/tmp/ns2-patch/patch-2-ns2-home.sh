#!/bin/bash
if [ "$1"x = x ]; then
MODIFY="sdn"
else
MODIFY=$1
fi

echo "move $MODIFY to ns home"

NS_HOME=~/bin/ns-allinone-2.35/ns-2.35
cp $MODIFY-ns-default.tcl $NS_HOME/tcl/lib/ns-default.tcl
cp $MODIFY-red.cc $NS_HOME/queue/red.cc
cp $MODIFY-tcp.cc $NS_HOME/tcp/tcp.cc
cp $MODIFY-tcp.h $NS_HOME/tcp/tcp.h
cp $MODIFY-tcp-full.cc $NS_HOME/tcp/tcp-full.cc
cp $MODIFY-tcp-full.h $NS_HOME/tcp/tcp-full.h
