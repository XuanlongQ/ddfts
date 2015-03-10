#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt

def get_flow_delay_cdf(input_file_name):

    input_file = open(input_file_name, 'r')
    rowList = input_file.readlines()
    table = [row.strip().split(' ') for row in rowList]
    input_file.close()
    flow_delay_list = [ float(x[0]) for x in table ]
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

#kwargs: label_dict['input_file_name'] output_file_name
def plot_flow_delay(input_file_name_list, **kwargs):

    #plt.plot(bins, pdf)
    l = len(input_file_name_list)

    color_list = ('blue', 'red', 'black', 'yellow', 'green', 'grey', 'pink', 'orange',)
    while len(color_list) < l:
        color_list += color_list

    linestyle_list = (':', '--', '-', )
    while len(linestyle_list) < l:
        linestyle_list += linestyle_list

    label_dict = {}
    if 'label_dict' in kwargs:
        label_dict = kwargs['label_dict']
    else:
        for i, input_file_name in zip(xrange(l), input_file_name_list):
            label_dict[input_file_name] = 'Test%03d'%(i+1)

    for i, input_file_name in zip(xrange(l), input_file_name_list):
            flow_delay_list, cdf, bins, pdf  = get_flow_delay_cdf(input_file_name)
            label = label_dict[input_file_name]
            color = color_list[i]
            linestyle = linestyle_list[i]
            #print 'linestyle = ' + linestyle
            plt.plot(flow_delay_list, cdf, color=color, linewidth=2.5, linestyle=linestyle, label=label)

    plt.xlim([-1, 10])

    plt.title('flow delay CDF')

    plt.xlabel('flow delay')

    plt.ylabel('CDF')

    plt.legend(loc = 'lower right')

    if 'plt_output' in kwargs:
        output = kwargs['plt_output']
        plt.savefig(output, dip=72)

    #plt.show()
    plt.clf()

if __name__ == '__main__':
    #read input file name (and output file name)
    #print len(sys.argv)
    input_plt = [ 'tmp/flow-delay-%02d.dat'%i for i in (1,2) ]
    
    import commands
    (status, output) = commands.getstatusoutput('mkdir -p out/tmp')
    print status, output
    plt_output  = 'out/tmp/flow-delay.png'

    plot_flow_delay(input_plt, plt_output = plt_output)
