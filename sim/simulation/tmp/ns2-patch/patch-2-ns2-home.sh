#!/bin/sh
NS_HOME=~/bin/ns-allinone-2.35/ns-2.35
cp d2tcp-red.c c$NS_HOME/queue/red.cc
cp d2tcp-tcp.cc $NS_HOME/tcp/tcp.cc
cp d2tcp-tcp.h $NS_HOME/tcp/tcp.h
cp d2tcp-tcp-full.cc $NS_HOME/tcp/tcp-full.cc
cp d2tcp-tcp-full.h $NS_HOME/tcp/tcp-full.h
