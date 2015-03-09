# Create your views here.
#encoding=utf-8
#from django.http import HttpResponse
from django.shortcuts import render_to_response, render

def home(request):
    print 'show home'
    print render(request, 'show/index.html', {'app_name':'Show'} )
    return render(request, 'show/index.html', {'app_name':'Show'} )
    #return render_to_response('show/index.html',)
