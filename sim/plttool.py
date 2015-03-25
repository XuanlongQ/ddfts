#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt

#ss: Simulation List
def plot_fd_cdf(s, output_file_name=None):

    flow_delay_list = [ float(f.end - f.start)/1000 for f in s.flow_set.all() ]

    bins = np.linspace(flow_delay_list[0], flow_delay_list[-1], 100)

    pdf = np.histogram(flow_delay_list, bins=bins, normed=False)[0]
    pdf = pdf*1.0/sum(pdf)
    cdf = [ sum(pdf[:i]) for i in xrange(1, len(pdf)+1)]

    plt.plot(bins[1:], cdf, color='r', linewidth=2.5, linestyle=':', label='flow delay cdf')
    i += 1

    #plt.xlim([0, 20])

    plt.title('flow delay CDF')

    plt.xlabel('flow delay(ms)')

    plt.ylabel('CDF')

    plt.legend(loc = 'lower right')

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

    bins = np.linspace(at_list[0], at_list[-1], 100)

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
    bins = np.arange(min(fsize) - sunit/2, max(fsize), sunit)
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
    #plt.plot(bins, bty_pdf, color='blue', linewidth=1.0, linestyle='--', label='Flow Bytes')

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
    tunit = 50000

    tbin = np.arange(sim_start, sim_end, tunit)
    tbin = tbin + tunit/2
    #print tbin
    fcnt = []
    for i in xrange(0, len(tbin)):
        trange = (tbin[i]-tunit/2,tbin[i]+tunit/2)
        #print trange
        fc = s.flow_set.all().filter(start__range=trange) | s.flow_set.all().filter(end__range=trange)
        #print fc
        fcnt.append(len(fc))
    #print 'fcnt:'
    #print fcnt 

    bins = np.arange(min(fcnt)-1, max(fcnt)+1)
    pdf = np.histogram(fcnt, bins=bins, density=False)[0]
    pdf = pdf*1.0/sum(pdf)
    cdf = [ sum(pdf[:i]) for i in xrange(1, len(pdf)+1)]
    bins = bins[1:]
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

#plot cdf of dropped packet count by time
#input: s(models.Simulation)
def plot_cc_cdf(s, output_file_name):
    pass
