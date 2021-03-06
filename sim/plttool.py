#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
import numpy as np
import simtool

import matplotlib
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
matplotlib.use('Agg')
print 'matplotlib.use("Agg")'
import matplotlib.pyplot as plt
xmajorLocator   = MultipleLocator(5) #将x主刻度标签设置为20的倍数
xmajorFormatter = FormatStrFormatter('%5d') #设置x轴标签文本的格式
xminorLocator   = MultipleLocator(0.5) #将x轴次刻度标签设置为5的倍数


ymajorLocator   = MultipleLocator(10) #将y轴主刻度标签设置为0.5的倍数
ymajorFormatter = FormatStrFormatter('%10d') #设置y轴标签文本的格式
yminorLocator   = MultipleLocator(1) #将此y轴次刻度标签设置为0.1的倍数

def getbinspdfcdf(sample_list):
    if len(sample_list) <= 0: 
      return (0,), (0,), (0,),
    bins = np.linspace(min(sample_list), max(sample_list), 100)
    pdf = np.histogram(sample_list, bins=bins, normed=False)[0]
    pdf = pdf*1.0/sum(pdf)
    cdf = [ sum(pdf[:i]) for i in xrange(1, len(pdf)+1)]
    return bins[1:], pdf, cdf
    

#ss: Simulation List
def plot_fd_cdf(ss, output_file_name=None):

    i = 1
    sub_title = ['0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',]
    for s in ss:
        ftype_list = ['q', ] #query, 
        ftype = 'q' #query, 
        #flow_delay_list = [ float(f.end - f.start)/1000 for f in s.flow_set.filter(finished=True).filter(ftype=ftype) ]
        flow_list = filter(lambda ff: ff.finished == True, s.flow_list)
        flow_list = filter(lambda ff: ff.ftype == ftype, flow_list)
        flow_delay_list = [ float(f.end - f.start)/1000 for f in flow_list ]
        #flow_delay_list = filter(lambda d: d < 100, flow_delay_list)
        bins, pdf, cdf = getbinspdfcdf(flow_delay_list)
        plt.subplot(2, 2, i)
        #plt.plot(bins, pdf, label='%s flow delay pdf' % (ftype,))
        plt.plot(bins, pdf, label='')
        #plt.plot(bins, cdf, label='%s flow delay cdf' % (ftype,))
        plt.xlim([50, 55])
        plt.ylim([0, 0.1])
        plt.xlabel('flow delay(ms)')
        #plt.ylabel('CDF')
        plt.legend(loc = 'upper right', ) #fontsize=8)
        plt.title('(%s) %s' % (sub_title[i], s.tcptype), loc='center')
        i += 1
    #plt.suptitle('PDF of Small Flow Delay')
    plt.tight_layout()
    if output_file_name:
        plt.savefig(output_file_name, dip=72)

    #plt.show()
    plt.clf()

#plot cdf of time between query arrivals
#input: s(models.Simulation)
def plot_qat_cdf(s, output_file_name):

    start_list = [ float(f.start)/1000000 for f in s.flow_set.all().filter(ftype='q').order_by('start') ]
    #when query comes to MLA, MLA split this query into n queries(flow), so we need to converge this n-query into one query
    start_list = list(set(start_list))
    start_list.sort()
    #time between arrival list
    at_list = [ (start_list[i] - start_list[i-1]) for i in xrange(1, len(start_list)) ]

    bins, pdf, cdf = getbinspdfcdf(at_list)

    plt.plot(bins, cdf, color='r', linewidth=2.5, linestyle='--', label='cdf')
    plt.plot(bins, pdf, color='b', linewidth=2.5, linestyle=':', label='pdf')

    #plt.xlim([0,2])
    plt.title('CDF of time between query arrivals')
    plt.xlabel('query flow start time(s)')
    plt.ylabel('CDF')
    plt.legend(loc = 'right')

    if output_file_name:
        plt.savefig(output_file_name, dip=72)

    #plt.show()
    plt.clf()

#plot cdf of time between background flow(short, large) arrivals
#input: s(models.Simulation)
def plot_bat_cdf(s, output_file_name=None):

    start_list = [ float(f.start)/1000000 for f in s.flow_set.all().exclude(ftype='q').order_by('start') ]
    #time between arrival list
    at_list = [ (start_list[i] - start_list[i-1]) for i in xrange(1, len(start_list)) ]

    bins, pdf, cdf = getbinspdfcdf(at_list)
    plt.plot(bins, cdf, color='r', linewidth=2.5, linestyle='--', label='cdf')
    plt.plot(bins, pdf, color='b', linewidth=2.5, linestyle=':', label='pdf')

    #plt.xlim([0, 20])
    plt.title('CDF of time between background flow arrivals')
    plt.xlabel('background flow start time(s)')
    plt.ylabel('CDF')
    plt.legend(loc = 'lower right')

    if output_file_name:
        plt.savefig(output_file_name, dip=72)

    #plt.show()
    plt.clf()

#plot background flow size's cdf
#input: s(models.Simulation)
def plot_bfs_cdf(s, output_file_name):

    fsize_list = [ f.size for f in s.flow_set.exclude(ftype='q')]

    bins, pdf, cdf = getbinspdfcdf(fsize_list)
    plt.plot(bins, pdf, color='black', linewidth=1.0, linestyle='-', label='Flow Count PDF')
    plt.plot(bins, cdf, color='blue', linewidth=1.0, linestyle=':', label='Flow Count CDF')

    #plt.xlim([0, 10])
    #plt.ylim([0, 0.1])

    plt.title('PDF of background flow size')
    plt.xlabel('flow size(Bytes)')
    plt.ylabel('CDF')
    plt.legend(loc = 'right')

    if output_file_name:
        plt.savefig(output_file_name, dip=72)

    #plt.show()
    plt.clf()

#plot cdf of concurrent connections
#input: s(models.Simulation)
def plot_cc_cdf(s, output_file_name):

    sim_start = 0 #simulation start time
    sim_end = 10000000 #simulation end time
    tunit = 50000 #50ms

    tbin = np.arange(sim_start, sim_end, tunit)
    tbin = tbin + tunit/2
    #print tbin
    fcnt_list = []
    for i in xrange(0, len(tbin)):
        trange = (tbin[i]-tunit/2,tbin[i]+tunit/2)
        #print trange
        flow_list = s.flow_set.all().filter(start__range=trange) | s.flow_set.all().filter(end__range=trange)
        #we want the average count of active flow in every server
        fc = (len(flow_list) * 1.0) / (simtool.SG * simtool.SC)
        #print fc
        fcnt_list.append(fc)
    #print 'fcnt_list:'
    #print fcnt_list 

    bins, pdf, cdf = getbinspdfcdf(fcnt_list)
    plt.plot(bins, pdf, color='black', linewidth=1.0, linestyle='-', label='Cuncurrent Connections PDF')
    plt.plot(bins, cdf, color='blue', linewidth=1.0, linestyle=':', label='Cuncurrent Connections CDF')

    #plt.xlim([0, 4])
    #plt.ylim([0, 0.05])

    plt.title('PDF of Concurrent Connections')
    plt.xlabel('Concurrent Connections')
    plt.ylabel('PDF')
    plt.legend(loc = 'upper left')

    if output_file_name:
        plt.savefig(output_file_name, dip=72)

    #plt.show()
    plt.clf()

#plot cdf of queue length by time
#input: s(models.Simulation)
def plot_ql_cdf(ss, output_file_name):
    i = 1
    sub_title = ['0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',]
    for s in ss:
        #qrecord = s.qrecord_set.all()
        qrecord = s.qrecord_list
        #print 'qrcord.len = ' , len(qrecord)
        time_dict = {}
        qlen_dict = {}
        for q in qrecord:
            qid = '%d,%d' % (q.rack, q.server)
            if not (qid in qlen_dict):
                time_dict[qid] = []
                qlen_dict[qid] = []
            time_dict[qid].append(q.time) 
            qlen_dict[qid].append(q.pktcnt) 
        plt.subplot(2, 2, i)
        for qid in time_dict:
            #print 'qid = ', qid
            time_list = map(lambda t: t/1000.0, time_dict[qid])
            qlen_list = qlen_dict[qid]
            plt.plot(time_list, qlen_list)

        plt.xlim([0, 1.5])
        #plt.ylim([0, 300])
        #plt.title('PDF of queue length')
        plt.title('(%s) %s'% (sub_title[i], s.tcptype))
        plt.xlabel('time(ms)')
        plt.ylabel('PDF fo queue length')
        i += 1
    
    plt.tight_layout()
    if output_file_name:
        plt.savefig(output_file_name, dip=72)
    plt.clf()

#plot cwnd by time
#input: s(models.Simulation)
def plot_cw_cdf(ss, output_file_name):
    i = 1
    sub_title = ['0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',]
    for s in ss:
        #cwnd_list = s.cwnd_set.all().order_by('time')
        cwnd_list = s.cwnd_list
        #print 'qrcord.len = ' , len(qrecord)
        time_list = []
        qf_list = []
        sf_list = []
        lf_list = []
        af_list = []
        for c in cwnd_list:
            time_list.append(c.time/1000.0)
            qf_list.append(c.qf)
            sf_list.append(c.sf)
            lf_list.append(c.lf)
            af_list.append(c.qf+c.lf)

        ax = plt.subplot(2, 2, i)
        #plt.plot(time_list, qf_list, label='small flow cwnd', )
        plt.plot(time_list, lf_list, label='large flow cwnd', )
        #plt.plot(time_list, af_list, label='flow cwnd', )

        #plt.xlim([0.0, 1.5])
        plt.ylim([0, 55])
        plt.title('(%s) %s'% (sub_title[i], s.tcptype))
        plt.xlabel('time(ms)')
        plt.ylabel('congestion window')
        plt.legend(loc = 'upper left', fontsize = 8)
        i += 1

        #设置主刻度标签的位置,标签文本的格式
        ax.xaxis.set_major_locator(xmajorLocator)
        ax.xaxis.set_major_formatter(xmajorFormatter)

        ax.yaxis.set_major_locator(ymajorLocator)
        ax.yaxis.set_major_formatter(ymajorFormatter)

        #显示次刻度标签的位置,没有标签文本
        ax.xaxis.set_minor_locator(xminorLocator)
        ax.yaxis.set_minor_locator(yminorLocator)

        ax.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度
        ax.yaxis.grid(True, which='minor') #y坐标轴的网格使用次刻度

    plt.tight_layout()
    if output_file_name:
        plt.savefig(output_file_name, dip=72)
        plt.savefig('%s.pdf' % (output_file_name), dip=72)
    plt.clf()

#plot throughput
#input: ss(models.Simulation list)
def plot_thrput(ss, output_file_name):

    lf_thrput_list = []
    qf_thrput_list = []
    tcptype_list = []
    ind = [ i*1. for i in range(len(ss))]
    width = 0.35
    for s in ss:
        tcptype_list.append(s.tcptype)
        lf_thrput = 0
        qf_thrput = 0
        large_flow_list = filter(lambda ff: ff.ftype == 'l', s.flow_list)
        query_flow_list = filter(lambda ff: ff.ftype == 'q', s.flow_list)
        for f in large_flow_list:
            lf_thrput += f.thrput
        for f in query_flow_list:
            qf_thrput += f.thrput
        lf_thrput_list.append(lf_thrput / (1024.*1024.))
        qf_thrput_list.append(qf_thrput / (1024.*1024.))

    #print 'len(ind):', ind
    #print 'len(lf_thrput_list):', len(lf_thrput_list)
    #print 'len(qf_thrput_list):', len(qf_thrput_list)
    print '(lf_thrput_list):', lf_thrput_list
    print '(qf_thrput_list):', qf_thrput_list
    lf = plt.bar(ind, lf_thrput_list, width, color='#9999ff')
    qf = plt.bar(ind, qf_thrput_list, width, bottom=lf_thrput_list, color='#ff9999')
    ind_ = [ i + width/2. for i in ind]
    plt.xticks(ind_ , tcptype_list )
    #plt.xlim([0, 10])
    plt.ylim([0, 120])

    plt.legend( (lf[0], qf[0]), ('Large Flow', 'Small Flow'), loc = 'upper right')
    plt.ylabel('Throughput(MB)')

    plt.tight_layout()
    if output_file_name:
        plt.savefig(output_file_name, dip=72)

    #plt.show()
    plt.clf()
