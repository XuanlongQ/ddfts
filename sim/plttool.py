#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
import numpy as np
import simtool

import matplotlib
matplotlib.use('Agg')
print 'matplotlib.use("Agg")'
import matplotlib.pyplot as plt

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
            time_list = map(lambda t: t/1000000.0, time_dict[qid])
            qlen_list = qlen_dict[qid]
            plt.plot(time_list, qlen_list)

        #plt.xlim([0, 4])
        #plt.ylim([0, 300])
        #plt.title('PDF of queue length')
        plt.title('(%s) %s'% (sub_title[i], s.tcptype))
        plt.xlabel('time(s)')
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
            time_list.append(c.time/1000000.0)
            qf_list.append(c.qf)
            sf_list.append(c.sf)
            lf_list.append(c.lf)
            af_list.append(c.qf+c.lf)

        plt.subplot(2, 2, i)
        plt.plot(time_list, qf_list, label='small flow cwnd', )
        plt.plot(time_list, lf_list, label='large flow cwnd', )
        plt.plot(time_list, af_list, label='flow cwnd', )

        #plt.xlim([450, 850])
        plt.ylim([0, 450])
        plt.title('(%s) %s'% (sub_title[i], s.tcptype))
        plt.xlabel('time(s)')
        plt.ylabel('congestion window')
        plt.legend(loc = 'upper left', fontsize = 8)
        i += 1

    plt.tight_layout()
    if output_file_name:
        plt.savefig(output_file_name, dip=72)
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
    plt.ylim([0, 140])

    plt.legend( (lf[0], qf[0]), ('Large Flow', 'Small Flow'), loc = 'upper right')
    plt.ylabel('Throughput(MB)')

    plt.tight_layout()
    if output_file_name:
        plt.savefig(output_file_name, dip=72)

    #plt.show()
    plt.clf()

#plot throughput
#input: ssss(models.Simulation list)
def plot_thrput_2(sss, output_file_name):
    i = 1
    width = 0.18
    sub_title = ['0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',]
    colors = ['#9999ff','#ffff99','#5555aa','#aaaa55',]
    for lfc in xrange(1, 5):
        plt.subplot(2, 2, i)
        line_dict = {}
        bars = []
        tcptypes = ['tcp', 'dctcp', 'd2tcp', 'sdnd2tcp']
        for j in xrange(0, len(tcptypes)):
            tcptype = tcptypes[j]
            color = colors[j]
            ss = filter(lambda s: s.lfc == lfc and s.tcptype == tcptype, sss)
            ss = sorted(ss, key=lambda s:s.sc)
            if len(ss) == 0:
                continue
            sndc_list = [ (s.sc - 1) for s in ss] #count of sender
            thrput_list = [ (s.qf_thrput + s.lf_thrput) / (1024.*1024.) for s in ss]
            #print 'sndc_list:', sndc_list
            #print 'thrput_list:', thrput_list
            line_dict[tcptype] = {'x':sndc_list, 'y':thrput_list}
            sndc_list_ = [ k + (j-2)*width for k in sndc_list]
            line_dict[tcptype]['bar'] = plt.bar(sndc_list_, thrput_list, width, color = color)
            bars.append(line_dict[tcptype]['bar'][0])
            #plt.plot(sndc_list, thrput_list, label=tcptype, )

        plt.xlim([30, 42])
        plt.ylim([107, 111.5])
        plt.title('(%s) %d large flow(s)'% (sub_title[i], lfc))
        plt.legend( bars, tcptypes, loc = 'upper right', fontsize = 7)
        plt.xlabel('number of sender')
        plt.ylabel('all flow throughput(MB)')
        #plt.legend(loc = 'upper right', fontsize = 8)
        i += 1

    plt.tight_layout()
    if output_file_name:
        plt.savefig(output_file_name, dip=72)
        plt.savefig('%s.pdf' % (output_file_name), dip=72)
    plt.clf()

#plot query count
#input: ssss(models.Simulation list)
def plot_qc(sss, output_file_name):
    i = 1
    width = 0.18
    sub_title = ['0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',]
    colors = ['#9999ff','#ffff99','#5555aa','#aaaa55',]
    for lfc in xrange(1, 5):
        plt.subplot(2, 2, i)
        line_dict = {}
        bars = []
        tcptypes = ['tcp', 'dctcp', 'd2tcp', 'sdnd2tcp']
        for j in xrange(0, len(tcptypes)):
            tcptype = tcptypes[j]
            color = colors[j]
            ss = filter(lambda s: s.lfc == lfc and s.tcptype == tcptype, sss)
            ss = sorted(ss, key=lambda s:s.sc)
            if len(ss) == 0:
                continue
            sndc_list = [ (s.sc - 1) for s in ss] #count of sender
            qc_list = [ (s.qfc)*1.0 / (s.sc - 1) for s in ss]
            line_dict[tcptype] = {'x':sndc_list, 'y':qc_list}
            sndc_list_ = [ k + (j-2)*width for k in sndc_list]
            line_dict[tcptype]['bar'] = plt.bar(sndc_list_, qc_list, width, color = color)
            bars.append(line_dict[tcptype]['bar'][0])
            #plt.plot(sndc_list, qc_list, label=tcptype, )

        plt.xlim([30, 42])
        plt.ylim([0, 11])
        plt.title('(%s) %d large flow(s)'% (sub_title[i], lfc))
        plt.legend( bars, tcptypes, loc = 'upper right', fontsize = 7)
        plt.xlabel('number of sender')
        plt.ylabel('count of query')
        plt.legend(loc = 'upper right', fontsize = 8)
        i += 1

    plt.tight_layout()
    if output_file_name:
        plt.savefig(output_file_name, dip=72)
        plt.savefig('%s.pdf' % (output_file_name), dip=72)
    plt.clf()
