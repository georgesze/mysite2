#coding:utf-8
 
from django.shortcuts import render
from django.views.decorators import csrf
from disk.models import AliConfig
 
 
# 接收POST请求数据
def Calculate(request):
    agent_list = AliConfig.objects.all()
    agent_dict = {'agents': agent_list}
    
    
    return render(request, "payslip.html", agent_dict)