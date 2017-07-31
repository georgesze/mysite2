#coding:utf-8
 
from django.shortcuts import render
from django.views.decorators import csrf
from disk.models import AliConfig
 
 
# 接收POST请求数据
def AgentPay(request):
    #拿到所有agent配置
    agent_list = AliConfig.objects.all()
    #agent_dict = {'agents': agent_list}
    
    # context must be dict type rather than query set
#    return render(request, "payslip.html", agent_dict)
    return render(request, "payslip.html", {'queryset': agent_list})