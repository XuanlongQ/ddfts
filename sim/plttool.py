#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt

#s: Simulation
def get_flow_delay_cdf(s):

    flow_delay_list = [ float(f.end - f.start)/1000000 for f in s.flow_set.all() ]
    print 'flow_delay_list ',len(flow_delay_list)
    flow_delay_list.sort()
    #print flow_delay_list
    n = len(flow_delay_list)

    bins = np.linspace(flow_delay_list[0], flow_delay_list[-1], 100)

    pdf = []
    pdf.append(0)
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

    plt.xlim([-1, 10])

    plt.title('flow delay CDF')

    plt.xlabel('flow delay')

    plt.ylabel('CDF')

    plt.legend(loc = 'lower right')

    if output_file_name:
        plt.savefig(output_file_name, dip=72)

    plt.show()
    plt.clf()
