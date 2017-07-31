#coding:utf-8
 
from django.shortcuts import render
from django.views.decorators import csrf
from disk.models import AliConfig,AliOrd
 
 
# 接收POST请求数据
def AgentPay(request):
    #拿到所有agent配置
    agent_list = AliConfig.objects.all()
    #agent_dict = {'agents': agent_list}
    
    # context must be dict type rather than query set
#    return render(request, "payslip.html", agent_dict)
    return render(request, "payslip.html", {'queryset': agent_list})



def Agent(request, agent_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a order name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        current_agent = AliConfig.objects.get(slug=agent_name_slug)
        context_dict['agent_name'] = AliConfig.AgentId

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        agent_orders = Page.objects.filter(order=order)

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


