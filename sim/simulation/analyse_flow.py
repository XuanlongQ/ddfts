def analyse_flow(input_file_name, output_file_name='out.dat'):
    highest_flow_id = 0
    input_file = open(input_file_name, 'r')
    stime_dict = {} #start time for each flow
    etime_dict = {} #end time
    fsize_dict = {} #flow size
    drcnt_dict = {} #drop packet count for each flow
    for line in input_file:
        #print len(line.strip().split(' '))
        action, time, frm, to, tp, pktsize, flag, flow_id, src, dst, seq_no, packet_id = line.strip().split(' ')
        time = float(time)
        pktsize = int(pktsize)

        if not flow_id in stime_dict:
            stime_dict[flow_id] = time
        if not flow_id in fsize_dict:
            fsize_dict[flow_id] = 0
        if not flow_id in drcnt_dict:
            drcnt_dict[flow_id] = 0

        dst_node, dst_port = dst.split('.')
        if action == 'r' and to == dst_node:
            etime_dict[flow_id] = time
            fsize_dict[flow_id] += pktsize
        else:
            etime_dict[flow_id] = -1
            if action == 'd':
                drcnt_dict[flow_id] += 1

    input_file.close()
    #
    id_list = sorted(stime_dict.keys(), lambda x,y: cmp(int(x),int(y)))
    output_file = open(output_file_name, 'w')
    for flow_id in id_list:
        start = stime_dict[flow_id]
        end = etime_dict[flow_id]
        duration = end - start
        fsize = fsize_dict[flow_id]
        drcnt = drcnt_dict[flow_id]
        line = '%s %f %d %d\n' % (flow_id, duration, fsize, drcnt)
        if start < end:
            #print 'flow %s: duration = %f, fsize=%d, drcnt = %d' % (flow_id, duration, fsize, drcnt)
            #print line,
            pass
        output_file.write(line)
    output_file.close()
if __name__ == '__main__':
    input_file_name = 'out.tr'
    analyse_flow(input_file_name)
