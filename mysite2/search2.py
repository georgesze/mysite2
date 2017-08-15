#coding:utf-8 
from django.shortcuts import render
from django.views.decorators import csrf
from django.db.models import Count, Min, Sum, Avg
from disk.models import AliConfig,AliOrd
from django import forms
from django.db import transaction

import datetime


class SearchForm(forms.Form):
    #title = forms.CharField(max_length=50)
    period_str = forms.DateField(initial=datetime.date(2017, 6, 1),widget=forms.SelectDateWidget())
    period_end = forms.DateField(initial=datetime.date(2017, 6, 30),widget=forms.SelectDateWidget())

   
# 接收POST请求数据
def AgentList(request):
    #拿到所有agent配置
    agent_list = AliConfig.objects.all()
    Incometotal = 0
      
    if (request.method == "POST") and ('calculate_income' in request.POST):
        form = SearchForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data.get('period_str')
            request.session['start'] = str(start)
            
            end = form.cleaned_data.get('period_end') + datetime.timedelta(days=1)
            request.session['end'] = str(end)
            
            #html request 不支持python date格式，需要转换 ????
            start = request.session.get('start')
            end = request.session.get('end')
            start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.datetime.strptime(end, "%Y-%m-%d").date()

            #取到所有代理列表            
            #agent_list = AliConfig.objects.filter()
            agent_list = AliConfig.objects.all()
            
            #取到期间总金额 from upload
            aggregated = AliOrd.objects.filter(SettleDate__range=(start, end)).aggregate(total=Sum('RebateAmt'))      
            Incometotal = aggregated['total']
                            
            # 遍历所有 代理 计算
            for agent in agent_list:
                # 计算所有订单佣金 volume 2000+
                CalculateOrderAgent(agent,start,end)
                
                CalculateOrderAmount(agent,start,end)
            
                # 计算收入 个人订单收入 + 一级下线贡献佣金 + 二级下线贡献佣金
                CalculateIncome(agent,start,end)
            
    elif (request.method == "POST") and ('display_income' in request.POST):
        form = SearchForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data.get('period_str')
            request.session['start'] = str(start)
            
            end = form.cleaned_data.get('period_end') + datetime.timedelta(days=1)
            request.session['end'] = str(end)
            
            #html request 不支持python date格式，需要转换 ????
            start = request.session.get('start')
            end = request.session.get('end')
            start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.datetime.strptime(end, "%Y-%m-%d").date()

            #取到所有代理列表            
            #agent_list = AliConfig.objects.filter()
            agent_list = AliConfig.objects.all()
            
            #取到期间总金额 from upload CSV file
            aggregated = AliOrd.objects.filter(SettleDate__range=(start, end)).aggregate(total=Sum('RebateAmt'))      
            Incometotal = aggregated['total']        
            
            # 遍历所有 代理 计算
            for agent in agent_list:
                # 计算收入 个人订单收入 + 一级下线贡献佣金 + 二级下线贡献佣金
                CalculateIncome(agent,start,end)
                
    else:
        form = SearchForm()
   
    aggregated = AliConfig.objects.all().aggregate(total=Sum('IncomeTotal'))      
    CollectSum = aggregated['total']   
         
    return render(request, "payslip.html", {'form_agent':agent_list,
                                            'form_period':form,
                                            'Incometotal':Incometotal,
                                            'CollectSum':CollectSum})

def AgentDetail(request, agent_name_slug):
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


def CalculateOrderAgent(agent,start,end):
    agent_pid = agent.AgentId.AgentId
    orders = AliOrd.objects.filter(PosID=agent_pid,SettleDate__range=(start, end))
    
    l_UplineId = None
    l_UplineName = None
    l_Up2lineId = None
    l_Up2lineName = None
    
    if not agent.AgentUpId == None:    
        l_UplineId = str(agent.AgentUpId.AgentId)        #上线ID
        l_UplineName = agent.AgentUpId.AgentName         #上线名称
        

        if not agent.AgentUpId.AId.AgentUpId == None:
            l_Up2lineId = str(agent.AgentUpId.AId.AgentUpId.AgentId)    #上上线ID
            l_Up2lineName = agent.AgentUpId.AId.AgentUpId.AgentName     #上上线名称  

    AliOrd.objects.filter(PosID=agent_pid,SettleDate__range=(start, end)).update(UplineId=l_UplineId,
                                                                                 UplineName=l_UplineName,
                                                                                 Up2lineId=l_Up2lineId,
                                                                                 Up2lineName=l_Up2lineName,
                                                                                 IncomePercSelf = agent.AgentPerc,
                                                                                 SharePercUp1 = agent.Agent2rdPerc,
                                                                                 SharePercUp2 = agent.Agent3rdPerc)        
    
@transaction.atomic
def CalculateOrderAmount(agent,start,end):
    # get aggent orders
    agent_pid = agent.AgentId.AgentId
    orders = AliOrd.objects.filter(PosID=agent_pid,SettleDate__range=(start, end))    
    
    for order_item in orders:
        update_flag = False
                
        l_temp = round(order_item.RebateAmt * agent.AgentPerc,2)
        if not order_item.IncomeSelf == l_temp:
            update_flag = True
            order_item.IncomeSelf = l_temp    
                
        l_temp = round(order_item.RebateAmt * agent.Agent2rdPerc,2)
        if not order_item.ShareUp1 == l_temp:
            update_flag = True
            order_item.ShareUp1 = l_temp                     
                    
        l_temp = round(order_item.RebateAmt * agent.Agent3rdPerc,2)
        if not order_item.ShareUp2 == l_temp:
            update_flag = True
            order_item.ShareUp2 = l_temp 
                                  
#                 order_item.IncomeSelf = order_item.RebateAmt * agent.AgentPerc    #自获佣金 
#                 order_item.ShareUp1 = order_item.RebateAmt * agent.Agent2rdPerc       #贡献上级佣金 
#                 order_item.ShareUp2 = order_item.RebateAmt * agent.Agent3rdPerc     #贡献上上级佣金  
        if update_flag == True:
            order_item.save(update_fields=['IncomeSelf','ShareUp1','ShareUp2'])
                    
#    transaction.commit()

    
#     for order_item in orders:
#         order_item.IncomeSelf = order_item.RebateAmt * agent.AgentPerc    #自获佣金 
#         order_item.ShareUp1 = order_item.RebateAmt * agent.Agent2rdPerc       #贡献上级佣金 
#         order_item.ShareUp2 = order_item.RebateAmt * agent.Agent3rdPerc     #贡献上上级佣金  
#         order_item.save()
        
        
################################################################### old code               
#     for order_item in orders:  
#         # 计算佣金分成 ---- 计算使用RebateAmt结算金额 ----
#         #计算个人所得佣金    
#         order_item.IncomePercSelf = agent.AgentPerc             #自获佣金比例
#         order_item.IncomeSelf = order_item.RebateAmt * agent.AgentPerc    #自获佣金               
#                
#         #取得上线信息
#         if not agent.AgentUpId == None:
#             order_item.UplineId = str(agent.AgentUpId.AgentId)        #上线ID
#          
#         #计算上线分成佣金
#             if not order_item.UplineId =='':
#                 order_item.UplineName = agent.AgentUpId.AgentName       #上线名称
#                 order_item.SharePercUp1 = agent.Agent2rdPerc                #贡献上级佣金比例
#                 order_item.ShareUp1 = order_item.RebateAmt * agent.Agent2rdPerc       #贡献上级佣金
#         
#             if not agent.AgentUpId.AId.AgentUpId == None:
#                 
#         
#                  #计算上上线分成佣金
#                 order_item.Up2lineId = str(agent.AgentUpId.AId.AgentUpId.AgentId)    #上上线ID
#         
#                 if not order_item.Up2lineId =='':   
#                     order_item.Up2lineName = agent.AgentUpId.AId.AgentUpId.AgentName    #上上线名称   
#                     order_item.SharePercUp2 = agent.Agent3rdPerc                        #贡献上上级佣金比例
#                     order_item.ShareUp2 = order_item.RebateAmt * agent.Agent3rdPerc     #贡献上上级佣金
#         
#         #保存计算结果
#         order_item.save()
    
    
        
        
def CalculateIncome(agent,start,end):
    agent_pid = agent.AgentId.AgentId   
    
    #个人订单收入
    aggregated1 = AliOrd.objects.filter(PosID=agent_pid,SettleDate__range=(start, end)).aggregate(Income=Sum('RebateAmt'))
    if aggregated1['Income'] == None:
        agent.IncomeSelf = 0
    else:       
        agent.IncomeSelf = aggregated1['Income'] * agent.AgentPerc

    #一级下线贡献佣金   
    aggregatedLv1 = AliOrd.objects.filter(UplineId=agent_pid,SettleDate__range=(start, end)).aggregate(IncomeLv1=Sum('RebateAmt'))
    if aggregatedLv1['IncomeLv1'] == None:
        agent.IncomeLv1 = 0
    else:       
        agent.IncomeLv1 = aggregatedLv1['IncomeLv1'] * agent.Agent2rdPerc  
          
    # 二级下线贡献佣金
    aggregatedLv2 = AliOrd.objects.filter(Up2lineId=agent_pid,SettleDate__range=(start, end)).aggregate(IncomeLv2=Sum('RebateAmt'))
    if aggregatedLv2['IncomeLv2'] == None:
        agent.IncomeLv2 = 0
    else:       
        agent.IncomeLv2 = aggregatedLv2['IncomeLv2'] * agent.Agent3rdPerc    
    
    # 总佣金
    agent.IncomeTotal = agent.IncomeSelf + agent.IncomeLv1 + agent.IncomeLv2
    
    #保存计算结果
    agent.save()
    
    
              