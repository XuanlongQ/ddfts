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
    if 'dctcp' in request.POST:
        s = Simulation()
        dctcp = request.POST['dctcp']
        s.dctcp = True if dctcp == 'true' else False
        s.save()
    #return home(request)
    return HttpResponseRedirect('/sim')

@log
@check_sim_daemon
def flow(request):
    print 'sim flow'
    sim_list = Simulation.objects.filter(status = 2).exclude(flow = None)
    return render(request, 'sim/flow.html', {'sim_list':sim_list} )


from plttool import *
@log
@check_sim_daemon
def plot(request):
    print 'sim plot'
    sim_list = Simulation.objects.filter(status = 2).exclude(flow = None)
    img_tmp_dir, img_tmp_url = get_img_pos()
    img_dict = {}
    for sim in sim_list:
        fd_img = '%s/fd_img_%s.png' % (img_tmp_dir, sim.sid)
        fd_img_url = '%s/fd_img_%s.png' % (img_tmp_url, sim.sid)
        plot_flow_delay([sim], fd_img)
        qat_img = '%s/qat_img_%s.png' % (img_tmp_dir, sim.sid)
        qat_img_url = '%s/qat_img_%s.png' % (img_tmp_url, sim.sid)
        plot_qat_cdf(sim, qat_img)
        bat_img = '%s/bat_img_%s.png' % (img_tmp_dir, sim.sid)
        bat_img_url = '%s/bat_img_%s.png' % (img_tmp_url, sim.sid)
        plot_bat_cdf(sim, bat_img)
        #background flow size's cdf
        bfs_img = '%s/bfs_img_%s.png' % (img_tmp_dir, sim.sid)
        bfs_img_url = '%s/bfs_img_%s.png' % (img_tmp_url, sim.sid)
        plot_bfs_cdf(sim, bfs_img)
        #concurrent connection cdf
        cc_img = '%s/cc_img_%s.png' % (img_tmp_dir, sim.sid)
        cc_img_url = '%s/cc_img_%s.png' % (img_tmp_url, sim.sid)
        plot_cc_cdf(sim, cc_img)

        img_dict[sim] = (qat_img_url, bat_img_url)
        img_dict[sim] = (qat_img_url, bat_img_url, bfs_img_url)
        img_dict[sim] = (fd_img_url, qat_img_url, bat_img_url, bfs_img_url)
        img_dict[sim] = (cc_img_url, fd_img_url, qat_img_url, bat_img_url, bfs_img_url)

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
