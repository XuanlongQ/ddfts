#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt

#s: Simulation
def get_flow_delay_cdf(s):

    flow_delay_list = [ float(f.end - f.start)/1000 for f in s.flow_set.all() ]
    flow_delay_list.sort()
    n = len(flow_delay_list)

    bins = np.linspace(flow_delay_list[0], flow_delay_list[-1], 100)

    pdf = [0]
    for i in xrange(1, len(bins)):
        pdf.append(len(np.array(filter(lambda a: a <= bins[i] and a > bins[i-1], flow_delay_list)))*1.0/n)

    cdf = [ len(np.array(filter(lambda a: a <= bi, flow_delay_list)))*1.0/n for bi in flow_delay_list ]
    #return (bins, pdf)
    return flow_delay_list, cdf, bins, pdf

#ss: Simulation List
def plot_flow_delay(ss, output_file_name=None):

    l = len(ss)

    color_list = ('blue', 'red', 'black', 'yellow', 'green', 'grey', 'pink', 'orange',)
    while len(color_list) < l:
        color_list += color_list

    linestyle_list = (':', '--', '-', )
    while len(linestyle_list) < l:
        linestyle_list += linestyle_list

    i = 0
    for s in ss:
        flow_delay_list, cdf, bins, pdf  = get_flow_delay_cdf(s)
        label = s.sid
        color = color_list[i]
        linestyle = linestyle_list[i]
        #print 'linestyle = ' + linestyle
        plt.plot(flow_delay_list, cdf, color=color, linewidth=2.5, linestyle=linestyle, label=label)
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
    at_list.sort()
    n = len(at_list)

    bins = np.linspace(at_list[0], at_list[-1], 100)

    pdf = [0]
    for i in xrange(1, len(bins)):
        pdf.append(len(np.array(filter(lambda a: a <= bins[i] and a > bins[i-1], at_list)))*1.0/n)

    cdf = [ len(np.array(filter(lambda a: a <= bi, at_list)))*1.0/n for bi in at_list ]
    at_list.insert(0, 0)
    cdf.insert(0, 0)

    plt.plot(at_list, cdf, color='r', linewidth=2.5, linestyle='--', label='cdf')
    plt.plot(bins, pdf, color='b', linewidth=2.5, linestyle=':', label='pdf')
    '''
    print 'start_list:'
    print start_list
    print 'at_list:'
    print at_list
    print 'bins:'
    print bins
    print 'pdf:'
    print pdf
    print 'cdf:'
    print cdf
    '''

    #plt.xlim([0,2])

    plt.title('CDF of time between query arrivals')

    plt.xlabel('query flow start time(s)')

    plt.ylabel('CDF')

    plt.legend(loc = 'lower right')

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
    at_list.sort()
    n = len(at_list)

    bins = np.linspace(at_list[0], at_list[-1], 100)

    pdf = [0]
    for i in xrange(1, len(bins)):
        pdf.append(len(np.array(filter(lambda a: a <= bins[i] and a > bins[i-1], at_list)))*1.0/n)

    cdf = [ len(np.array(filter(lambda a: a <= bi, at_list)))*1.0/n for bi in at_list ]

    plt.plot(at_list, cdf, color='r', linewidth=2.5, linestyle='--', label='cdf')
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

    n = len(s.flow_set.all())
    bins = [ i for i in xrange(0, 1000000, 10000) ]
    #cnt_pdf = [ len(s.flow_set.all().filter(size__range=(i, i+10000)))*1.0/n for i in bins ]
    cnt_pdf = []
    bty_pdf = []
    total_byte = 0.0
    for i in bins:
        fs = s.flow_set.all().filter(size__range=(i, i+10000))
        cnt_pdf.append(len(fs)*1.0/n)
        tmp_byte = 0.0
        for f in fs:
            tmp_byte += f.size
            total_byte += f.size
        bty_pdf.append(tmp_byte)

    for i in xrange(len(bty_pdf)):
        bty_pdf[i] = bty_pdf[i]/total_byte
            

    plt.plot(bins, cnt_pdf, color='black', linewidth=1.0, linestyle='-', label='Flow Count')
    plt.plot(bins, bty_pdf, color='blue', linewidth=1.0, linestyle='--', label='Flow Bytes')

    #plt.xlim([0, 10])
    plt.ylim([0, 0.05])

    plt.title('PDF of background flow size')

    plt.xlabel('flow size(Bytes)')

    plt.ylabel('CDF')

    plt.legend(loc = 'upper left')

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
    cnt_list = []
    print tbin
    for i in xrange(1, len(tbin)):
        #tbin[i-1] tbin[i] start end 
        #start end tbin[i-1] tbin[i]
        trange = (tbin[i-1],tbin[i])
        #print trange
        fc = s.flow_set.all().filter(start__range=trange) | s.flow_set.all().filter(end__range=trange)
        #print fc
        cnt_list.append(len(fc))
    cnt_list.sort()
    print 'cnt_list:'
    print cnt_list
    n = len(cnt_list)
    cunit = n/20
    bins = [ i for i in xrange(cnt_list[0], cnt_list[-1], cunit)]
    cnt_pdf = []
    for i in xrange(0,len(bins)):
       cnt_pdf.append(len(filter(lambda a: a>=bins[i] and a<bins[i]+cunit, bins))*1.0/n)

    plt.plot(bins, cnt_pdf, color='black', linewidth=1.0, linestyle='-', label='Cuncurrent Connections')

    #plt.xlim([0, 10])
    #plt.ylim([0, 0.05])

    plt.title('PDF of Concurrent Connections')

    plt.xlabel('Concurrent Connections')

    plt.ylabel('PDF')

    plt.legend(loc = 'upper left')

    if output_file_name:
        plt.savefig(output_file_name, dip=72)

    #plt.show()
    plt.clf()
