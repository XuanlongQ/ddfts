# Create your views here.
#encoding=utf-8
#from django.http import HttpResponse
from django.shortcuts import render_to_response, render

def home(request):
    print 'sim home'
    image_dict = get_image_dict()
    print 'image_dict', image_dict
    return render(request, 'sim/index.html', {'image_dict':image_dict} )
    #return render_to_response('sim/index.html',)
def get_image_dict():
    import os.path
    PROJECT_DIR = os.path.abspath(os.path.dirname(__name__))
    out_dir = '%s/simulation/out/'%(PROJECT_DIR)
    print out_dir
    if not os.path.exists(out_dir):
        print 'out_dir does not exist'
        return
    test_list = os.listdir(out_dir)
    image_dict = {}
    for test_id in test_list:
        plt_dir = '%s%s/plt'%(out_dir, test_id)
        if not os.path.exists(plt_dir):
            continue
        print plt_dir
        image_list = [ '%s/%s'%(plt_dir, image) for image in os.listdir(plt_dir) if image.endswith('.png')]
        #print 'image_list ', image_list
        image_dict[test_id] = image_list
    return image_dict
