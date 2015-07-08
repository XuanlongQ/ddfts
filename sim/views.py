# Create your views here.
#encoding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from models import *
import functools
import simtool
import time

def check_sim_daemon(f):
    @functools.wraps(f)
    def fn(*args, **argskw):
        print 'check simulation daemon'
        if simtool.SIM_DAEMON and simtool.SIM_DAEMON.is_alive():
            print 'simulation daemon is alive'
            return f(*args, **argskw)

        print 'simtool.SIM_DAEMON:', simtool.SIM_DAEMON
        if simtool.SIM_DAEMON:
            print 'simtool.SIM_DAEMON.is_alive():', simtool.SIM_DAEMON.is_alive()
        print 'simulation daemon is not alive, start it!!!'
        import threading
        from simtool import simulate_daemon
        daemon = threading.Thread(target=simulate_daemon, args=('simulate daemon',))
        daemon.setDaemon(True)
        daemon.start()
        simtool.SIM_DAEMON = daemon
        return f(*args, **argskw)
    return fn
def log(f):
    @functools.wraps(f)
    def fn(*args, **argskw):
        print 'call sim.%s' % (f.__name__, )
        return f(*args, **argskw)
    return fn

@log
@check_sim_daemon
def home(request):
    print 'sim home'

    flow_list = Flow.objects.all()
    sim_list = Simulation.objects.all()
    return render(request, 'sim/index.html', {'sim_list':sim_list} )
    #return render_to_response('sim/index.html',)

@log
@check_sim_daemon
def addsim(request):
    print 'addsim'
    if 'tcptype' in request.POST:
        s = Simulation()
        tcptype = request.POST['tcptype']
        s.tcptype = tcptype.lower()
        s.save()
    #return home(request)
    return HttpResponseRedirect('/sim')

@log
@check_sim_daemon
def flow(request):
    print 'sim flow'
    DONE = 2
    #sim_list = Simulation.objects.filter(status = DONE)
    sim_list = simtool.sim_list
    return render(request, 'sim/flow.html', {'sim_list':sim_list} )


from plttool import *
@log
@check_sim_daemon
def plot(request):
    print 'sim plot'
    DONE = 2
    sim_list = Simulation.objects.filter(status = DONE).exclude(flow = None)
    sim_list = simtool.sim_list
    img_tmp_dir, img_tmp_url = get_img_pos()
    img_dict = {}
    for sim in sim_list:
        cdf_plot = {}
        #flow delay cdf/pdf by flow
        cdf_plot['fd'] = plot_fd_cdf
        cdf_plot['ql'] = plot_ql_cdf
        cdf_plot['cw'] = plot_cw_cdf
        cdf_plot['tp'] = plot_thrput
        '''
        #query arrival time cdf/pdf by query flow
        cdf_plot['qat'] = plot_qat_cdf
        #background flow arrival time cdf/pdf by background flow
        cdf_plot['bat'] = plot_bat_cdf
        #background flow size's cdf by background flow
        cdf_plot['bfs'] = plot_bfs_cdf
        #concurrent connection cdf by time
        cdf_plot['cc'] = plot_cc_cdf
        #queue length cdf/pdf by time
        #cdf_plot['ql'] = plot_ql_cdf
        '''
        img_list = []
        for cdf, plot in cdf_plot.iteritems():
            img = '%s/%s_img_%s.png' % (img_tmp_dir, cdf, sim.sid)
            img_url = '%s/%s_img_%s.png' % (img_tmp_url, cdf, sim.sid)
            #print img
            #print img_url
            if img_url.find('fd') >= 0 and True:
                plot(sim_list, img)
                img_list.append(img_url)
                pass
            elif img_url.find('ql') >= 0 and True:
                plot(sim_list, img)
                img_list.append(img_url)
                pass
            elif img_url.find('cw') >= 0 and True:
                plot(sim_list, img)
                img_list.append(img_url)
                pass
            elif img_url.find('tp') >= 0 and True:
                plot(sim_list, img)
                img_list.append(img_url)
                pass
            else:
                plot(sim, img)
                #img_list.append(img_url)
                pass
        img_dict[sim] = img_list
        break

    return render(request, 'sim/plot.html', {'sim_list':sim_list, 'img_dict':img_dict} )

def get_img_pos():
    import os.path
    PROJECT_DIR = os.path.abspath(os.path.dirname(__name__))
    img_tmp_dir = '%s/sim/static/image/tmp'%(PROJECT_DIR)
    img_tmp_url = '/static/image/tmp'
    return img_tmp_dir, img_tmp_url

'''
def get_image_dict():
    import os.path
    PROJECT_DIR = os.path.abspath(os.path.dirname(__name__))
    out_dir = '%s/sim/simulation/out/'%(PROJECT_DIR)
    #print out_dir
    if not os.path.exists(out_dir):
        print 'out_dir does not exist'
        return
    test_list = os.listdir(out_dir)
    image_dict = {}
    for test_id in test_list:
        plt_dir = '%s%s/plt'%(out_dir, test_id)
        if not os.path.exists(plt_dir):
            continue
        #print plt_dir
        image_list = [ '/static/%s/plt/%s'%(test_id, image) for image in os.listdir(plt_dir) if image.endswith('.png')]
        image_list = sorted(image_list, reverse_cmp)
        #print 'image_list ', image_list
        image_dict[test_id] = image_list
    return image_dict

def reverse_cmp(x, y):
    b = 1
    if x > y:
        return -b
    if x < y:
        return b
    return 0
'''
