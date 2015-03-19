# Create your views here.
#encoding=utf-8
#from django.http import HttpResponse
from django.shortcuts import render_to_response, render

def home(request):
    print 'sim home'
    from models import Simulation, Flow
    s = Simulation()
    s.dctcp = False
    s.done = False
    s.save()
    from simtool import simulate
    s, flow_list = simulate(s)
    flow_list = Flow.objects.all()
    sim_list = Simulation.objects.all()
    image_dict = get_image_dict()
    #print 'image_dict', image_dict
    return render(request, 'sim/index.html', {'image_dict':image_dict, 'sim_list':sim_list} )
    #return render_to_response('sim/index.html',)

def flow(request):
    print 'sim flow'
    from models import Simulation
    sim_list = Simulation.objects.filter(done = True).exclude(flow = None)
    return render(request, 'sim/flow.html', {'sim_list':sim_list} )

def plot(request):
    print 'sim plot'
    from models import Simulation
    sim_list = Simulation.objects.filter(done = True).exclude(flow = None)
    from plttool import plot_flow_delay, plot_qat_cdf, plot_bat_cdf, plot_bfs_cdf
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

        img_dict[sim] = (qat_img_url, bat_img_url)
        img_dict[sim] = (qat_img_url, bat_img_url, bfs_img_url)
        img_dict[sim] = (fd_img_url, qat_img_url, bat_img_url, bfs_img_url)

    return render(request, 'sim/plot.html', {'sim_list':sim_list, 'img_dict':img_dict} )

def get_img_pos():
    import os.path
    PROJECT_DIR = os.path.abspath(os.path.dirname(__name__))
    img_tmp_dir = '%s/sim/static/image/tmp'%(PROJECT_DIR)
    img_tmp_url = '/static/image/tmp'
    return img_tmp_dir, img_tmp_url

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
