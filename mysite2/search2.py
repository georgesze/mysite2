#coding:utf-8
 
from django.shortcuts import render
from django.views.decorators import csrf
from django.db.models import Count, Min, Sum, Avg
from disk.models import AliConfig,AliOrd
from django import forms

import datetime

class SearchForm(forms.Form):
    #title = forms.CharField(max_length=50)
    period_str = forms.DateField(initial=datetime.date(2017, 6, 1),widget=forms.SelectDateWidget())
    period_end = forms.DateField(initial=datetime.date(2017, 6, 30),widget=forms.SelectDateWidget())

   
# 接收POST请求数据
def AgentList(request):
    #拿到所有agent配置
    agent_list = AliConfig.objects.all()
      
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data.get('period_str')
            request.session['start'] = str(start)
            
            end = form.cleaned_data.get('period_end')
            request.session['end'] = str(end)
            
            #html request 不支持python date格式，需要转换 ????
            start = request.session.get('start')
            end = request.session.get('end')
            start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.datetime.strptime(end, "%Y-%m-%d").date()

            #取到所有代理列表            
            #agent_list = AliConfig.objects.filter()
            agent_list = AliConfig.objects.all()
            
            for agent in agent_list:
                # 计算所有订单佣金 volume 2000+
                CalculateAgentOrder(agent,start,end)
                
                # 计算收入 个人订单收入 + 一级下线贡献佣金 + 二级下线贡献佣金
                CalculateIncome(agent,agent_list,start,end)
                
    else:
        form = SearchForm()
     
    # context must be dict type rather than query set
#    return render(request, "payslip.html", agent_dict)
    return render(request, "payslip.html", {'form_agent': agent_list,
                                            'form_period':form})



def Agent(request, agent_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a order name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        current_agent = AliConfig.objects.get(Slug=agent_name_slug)
        context_dict['agent_name'] = current_agent.AgentId.AgentName + current_agent.AgentId.AgentId

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        start = request.session.get('start')
        end = request.session.get('end')
        
        start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        
        # settle date 订单结算时间
        agent_orders = AliOrd.objects.filter(PosID=current_agent.AgentId.AgentId,SettleDate__range=(start, end))
        #agent_orders = AliOrd.objects.filter(PosID=current_agent.AgentId.AgentId,CreatDate__contains=datetime.date(2017,5,15))   CreatDate__contains=end
        
        #agent_orders = AliOrd.objects.all()
        

        # Adds our results list to the template context under name pages.
        context_dict['agent_orders'] = agent_orders
        # We also add the order object from the database to the context dictionary.
        # We'll use this in the template to verify that the order exists.
        context_dict['current_agent'] = current_agent
    except AliConfig.DoesNotExist:
        # We get here if we didn't find the specified order.
        # Don't do anything - the template displays the "no order" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'order.html', context_dict)


def CalculateAgentOrder(agent,start,end):
    agent_pid = agent.AgentId.AgentId
    orders = AliOrd.objects.filter(PosID=agent_pid,SettleDate__range=(start, end))
               
    for order_item in orders:  
        #取得上线信息
        order_item.UplineId = str(agent.AgentUpId.AgentId)        #上线ID
        
        # 计算佣金分成 ---- 计算使用SettleAmt结算金额 ----
        #计算个人所得佣金    
        order_item.IncomePercSelf = agent.AgentPerc             #自获佣金比例
        order_item.IncomeSelf = order_item.SettleAmt * agent.AgentPerc    #自获佣金        
        
        #计算上线分成佣金
        if not order_item.UplineId =='':
            order_item.UplineName = str(agent.AgentUpId.AgentName)       #上线名称
            order_item.SharePercUp1 = agent.Agent2rdPerc                #贡献上级佣金比例
            order_item.ShareUp1 = order_item.SettleAmt * agent.Agent2rdPerc       #贡献上级佣金
        
        #计算上上线分成佣金
        order_item.Up2lineId = str(agent.AgentUpId.AId.AgentUpId.AgentId)    #上上线ID
        
        if not order_item.Up2lineId =='':   
            order_item.Up2lineName = agent.AgentUpId.AId.AgentUpId.AgentName    #上上线名称   
            order_item.SharePercUp2 = agent.Agent3rdPerc                        #贡献上上级佣金比例
            order_item.ShareUp2 = order_item.SettleAmt * agent.Agent3rdPerc     #贡献上上级佣金
        
        #保存计算结果
        order_item.save()
        
def CalculateIncome(agent,agent_list,start,end):
    agent_pid = agent.AgentId.AgentId   
    
    #个人订单收入
    aggregated = AliOrd.objects.filter(PosID=agent_pid,SettleDate__range=(start, end)).aggregate(Income1=Sum('SettleAmt'))
    if aggregated['Income1'] == None:
        agent.IncomeSelf = 0
    else:       
        agent.IncomeSelf = aggregated['Income1'] * agent.AgentPerc

    #一级下线贡献佣金   
    
    
    # 二级下线贡献佣金
    
