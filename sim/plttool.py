#!/usr/bin/python
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
def plot_fd_cdf(s, output_file_name=None):

    ftype_list = ['a', 'q', 's', 'l'] # all, query, short, large
    ftype_list = ['q', ] #query, 
    for i, ftype in zip(range(1,5), ftype_list):
        if ftype == 'a':
            flow_delay_list = [ float(f.end - f.start)/1000 for f in s.flow_set.filter(finished=True) ]
        else:
            flow_delay_list = [ float(f.end - f.start)/1000 for f in s.flow_set.filter(finished=True).filter(ftype=ftype) ]

        #flow_delay_list = filter(lambda d: d < 100, flow_delay_list)

        bins, pdf, cdf = getbinspdfcdf(flow_delay_list)
        #plt.subplot(2, 2, i)
        plt.plot(bins, pdf, label='%s flow delay pdf' % (ftype,))
        #plt.plot(bins, cdf, label='%s flow delay cdf' % (ftype,))

        #plt.xlim([100, 500])
        plt.ylim([0, 1])
        #plt.title('%s flow delay CDF' % (ftype,))
        plt.xlabel('flow delay(ms)')
        #plt.ylabel('CDF')
        plt.legend(loc = 'upper right', ) #fontsize=8)

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
def plot_ql_cdf(s, output_file_name):
    qrecord = s.qrecord_set.all()
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
    for qid in time_dict:
        #print 'qid = ', qid
        time_list = time_dict[qid]
        qlen_list = qlen_dict[qid]
        plt.plot(time_list, qlen_list)

    #plt.xlim([0, 4])
    #plt.ylim([0, 300])
    plt.title('PDF of queue length')
    plt.xlabel('time')
    plt.ylabel('PDF fo queue length')
    if output_file_name:
        plt.savefig(output_file_name, dip=72)

    plt.clf()

#plot cwnd by time
#input: s(models.Simulation)
def plot_cw_cdf(s, output_file_name):
    cwnd_list = s.cwnd_set.all().order_by('time')
    #print 'qrcord.len = ' , len(qrecord)
    time_list = []
    qf_list = []
    sf_list = []
    lf_list = []
    af_list = []
    for c in cwnd_list:
        time_list.append(c.time/1000)
        qf_list.append(c.qf)
        sf_list.append(c.sf)
        lf_list.append(c.lf)
        af_list.append(c.qf+c.lf)

    plt.plot(time_list, qf_list, label="query flow cwnd", )
    plt.plot(time_list, lf_list, label="large flow cwnd", )
    plt.plot(time_list, af_list, label="all flow cwnd", )

    #plt.xlim([0, 4])
    #plt.ylim([0, 100])
    plt.title('congestion window')
    plt.xlabel('time(ms)')
    plt.ylabel('cwnd')
    plt.legend(loc = 'upper right')
    if output_file_name:
        plt.savefig(output_file_name, dip=72)

    plt.clf()
