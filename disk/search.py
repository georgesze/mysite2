#coding:utf-8 
 
from django.shortcuts import render
from django.views.decorators import csrf
 
# 接收POST请求数据
def search(request):  #action="/search"
    ctx ={}
    if request.POST:
        ctx['result_list'] = request.POST['calculate']
    return render(request, "search.html", ctx)