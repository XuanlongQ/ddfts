#!/usr/bin/python
import sys
import numpy as np
import matplotlib.pyplot as plt

def plot_flow_delay(input_file_name, out_put_file_name):

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

	plt.plot(flow_delay_list, cdf)

	#plt.plot(bins, pdf)

	plt.xlim([-1, 5])

	plt.title("flow delay CDF")

	plt.xlabel("flow delay")

	plt.ylabel("CDF")

	plt.show()

if __name__ == '__main__':
	#read input file name (and output file name)
	#print len(sys.argv)
	if len(sys.argv) < 2:
	    print 'please specify the input file'
	    exit(0)
	input_file_name = sys.argv[1]

	output_file_name = 'out/flow-delay.jpg'
	if len(sys.argv) >= 3:
	    output_file_name = sys.argv[2]
	plot_flow_delay(input_file_name, output_file_name)
