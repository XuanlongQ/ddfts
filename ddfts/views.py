#encoding=utf-8
#from django.http import HttpResponse
from django.shortcuts import render_to_response, render

def home(request):
    return render(request, 'index.html', {'statuse_list':'222'} )
