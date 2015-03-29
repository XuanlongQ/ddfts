#!/bin/sh
if [ "$2"x = x ]; then
MODIFY="modify"
else
MODIFY=$2
fi
NS_HOME=~/bin/ns-allinone-2.35/ns-2.35
cp $NS_HOME/queue/red.cc $MODIFY-red.cc
cp $NS_HOME/tcp/tcp.cc $MODIFY-tcp.cc
cp $NS_HOME/tcp/tcp.h $MODIFY-tcp.h
cp $NS_HOME/tcp/tcp-full.cc $MODIFY-tcp-full.cc
cp $NS_HOME/tcp/tcp-full.h $MODIFY-tcp-full.h
