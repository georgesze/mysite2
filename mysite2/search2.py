#coding:utf-8
 
from django.shortcuts import render
from django.views.decorators import csrf
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
        order_tiem.UplineId = agent.AgentId.AgentUpId           #上线ID
        order_tiem.UplineName = agent.AgentId.AgentName         #上线名称
        #order_tiem.Up2lineId = agent.AgentId.                     #上上线ID
        order_tiem.IncomePercSelf = agent.AgentPerc             #自获佣金比例
        order_tiem.SharePercUp1 = agent.Agent2rdPerc            #贡献上级佣金比例
        order_tiem.SharePercUp2 = agent.Agent3rdPerc    #贡献上上级佣金比例
        # 计算佣金分成 ---- 计算使用SettleAmt结算金额 ----
        order_tiem.IncomeSelf = order_item * agent.AgentPerc    #自获佣金
        order_tiem.ShareUp1 = order_item * agent.Agent2rdPerc   #贡献上级佣金
        order_tiem.ShareUp2 = order_item * agent.Agent3rdPerc   #贡献上上级佣金

        #计算个人所得佣金

        #计算上线分成佣金
  
        #计算上上线分成佣金
        
        #保存计算结果
        order_item.save()
