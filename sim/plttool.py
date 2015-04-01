#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt
import simtool

#ss: Simulation List
def plot_fd_cdf(s, output_file_name=None):

    flow_delay_list = [ float(f.end - f.start)/1000 for f in s.flow_set.filter(finished=True).filter(ftype='q') ]

    bins = np.linspace(min(flow_delay_list), max(flow_delay_list), 100)

    pdf = np.histogram(flow_delay_list, bins=bins, normed=False)[0]
    pdf = pdf*1.0/sum(pdf)
    cdf = [ sum(pdf[:i]) for i in xrange(1, len(pdf)+1)]

    plt.plot(bins[1:], pdf, label='flow delay pdf')
    plt.plot(bins[1:], cdf, label='flow delay cdf')

    plt.xlim([4000, 6500])
    plt.ylim([0, .0010])
    plt.title('flow delay CDF')
    plt.xlabel('flow delay(ms)')
    plt.ylabel('CDF')
    plt.legend(loc = 'upper right')

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

    bins = np.linspace(min(at_list), max(at_list), 100)

    pdf = np.histogram(at_list, bins=bins, normed=False)[0]
    pdf = pdf*1.0/sum(pdf)
    bins = bins[1:]
    cdf = [ sum(pdf[:i]) for i in xrange(1, len(pdf)+1)]

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

    bins = np.linspace(min(at_list), max(at_list), 100)

    pdf = np.histogram(at_list, bins=bins, normed=False)[0]
    pdf = pdf*1.0/sum(pdf)
    bins = bins[1:]
    cdf = [ sum(pdf[:i]) for i in xrange(1, len(pdf)+1)]


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

    fsize = [ f.size for f in s.flow_set.exclude(ftype='q')]
    #print fsize
    sunit = 1000000
    bins = np.linspace(min(fsize) - sunit/2, max(fsize), 100)
    #print bins
    #bins = np.array([0, 2001, 1000100, 10000000, 100000000,])
    pdf = np.histogram(fsize, bins=bins, density=False)[0]
    pdf = pdf*1.0/sum(pdf)
    bins = bins[1:] + sunit/2
    cdf = [ sum(pdf[:i]) for i in xrange(1, len(pdf)+1)]
    #print pdf
    #print cdf

    plt.plot(bins, pdf, color='black', linewidth=1.0, linestyle='-', label='Flow Count PDF')
    #plt.plot(bins, cdf, color='blue', linewidth=1.0, linestyle=':', label='Flow Count CDF')

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
    fcnt = []
    for i in xrange(0, len(tbin)):
        trange = (tbin[i]-tunit/2,tbin[i]+tunit/2)
        #print trange
        flow_list = s.flow_set.all().filter(start__range=trange) | s.flow_set.all().filter(end__range=trange)
        #we want the average count of active flow in every server
        fc = (len(flow_list) * 1.0) / (simtool.SG * simtool.SC)
        #print fc
        fcnt.append(fc)
    #print 'fcnt:'
    #print fcnt 

    bins = np.linspace(min(fcnt), max(fcnt), 100)
    pdf = np.histogram(fcnt, bins=bins, density=False)[0]
    pdf = pdf*1.0/sum(pdf)
    cdf = [ sum(pdf[:i]) for i in xrange(1, len(pdf)+1)]
    plt.plot(bins[1:], pdf, color='black', linewidth=1.0, linestyle='-', label='Cuncurrent Connections PDF')
    plt.plot(bins[1:], cdf, color='blue', linewidth=1.0, linestyle=':', label='Cuncurrent Connections CDF')

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
    plt.ylim([0, 300])
    plt.title('PDF of queue length')
    plt.xlabel('time')
    plt.ylabel('PDF fo queue length')
    if output_file_name:
        plt.savefig(output_file_name, dip=72)

    plt.clf()
