# coding:utf-8
from django.shortcuts import render
from django.views.decorators import csrf
from django.db.models import Count, Min, Sum, Avg
from disk.models import AliConfig, AliOrd, PayResult
from django import forms
from django.core import serializers
from django.db import transaction
from datetime import datetime
from django.http import HttpResponse

import datetime
import json
import decimal
import xlwt

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


class SearchForm(forms.Form):
    # title = forms.CharField(max_length=50)
    period_str = forms.DateField(initial=datetime.date(2017, 10, 1), widget=forms.SelectDateWidget())
    period_end = forms.DateField(initial=datetime.date(2017, 10, 31), widget=forms.SelectDateWidget())


# 接收POST请求数据    payslip 1
def AgentList(request):
    # 拿到所有agent配置
    agent_list = AliConfig.objects.all()
    Incometotal = 0

    if (request.method == "POST") and ('calculate_income' in request.POST):
        form = SearchForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data.get('period_str')
            request.session['start'] = str(start)

            end = form.cleaned_data.get('period_end') + datetime.timedelta(days=1)
            request.session['end'] = str(end)

            # html request 不支持python date格式，需要转换 ????
            start = request.session.get('start')
            end = request.session.get('end')
            start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.datetime.strptime(end, "%Y-%m-%d").date()

            # 取到所有代理列表
            # agent_list = AliConfig.objects.filter()
            agent_list = AliConfig.objects.all()

            # 取到期间总金额 from upload
            aggregated = AliOrd.objects.filter(SettleDate__range=(start, end)).aggregate(total=Sum('RebateAmt'))
            Incometotal = aggregated['total']

            # 遍历所有 代理 计算
            for agent in agent_list:
                # 计算所有订单佣金 volume 20000+
                CalculateOrderAgent(agent, start, end)

                CalculateOrderAmount(agent, start, end)

                # 计算收入 个人订单收入 + 一级下线贡献佣金 + 二级下线贡献佣金
                CalculateIncome(agent, start, end)

                # 保存月佣金计算记录
                save_pay_result(agent, start, end)

    elif (request.method == "POST") and ('display_income' in request.POST):
        form = SearchForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data.get('period_str')
            request.session['star   t'] = str(start)

            end = form.cleaned_data.get('period_end') + datetime.timedelta(days=1)
            request.session['end'] = str(end)

            # html request 不支持python date格式，需要转换 ????
            start = request.session.get('start')
            end = request.session.get('end')
            start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.datetime.strptime(end, "%Y-%m-%d").date()

            # 取到所有代理列表
            # agent_list = AliConfig.objects.filter()
            agent_list = AliConfig.objects.all()

            # 取到期间总金额 from upload CSV file
            aggregated = AliOrd.objects.filter(SettleDate__range=(start, end)).aggregate(total=Sum('RebateAmt'))
            Incometotal = aggregated['total']

            # 遍历所有 代理 计算
            for agent in agent_list:
                # 计算收入 个人订单收入 + 一级下线贡献佣金 + 二级下线贡献佣金
                CalculateIncome(agent, start, end)

    else:
        # form = SearchForm()
        form = SearchForm({'period_str': datetime.date(2017, 10, 1), 'period_end': datetime.date(2017, 10, 31)})
        if form.is_valid():
            start = form.cleaned_data.get('period_str')
            end = form.cleaned_data.get('period_end') + datetime.timedelta(days=1)
            request.session['start'] = str(start)
            request.session['end'] = str(end)

    aggregated = AliConfig.objects.all().aggregate(total=Sum('IncomeTotal'))
    CollectSum = aggregated['total']

    return render(request, "payslip.html", {'form_agent': agent_list,
                                            'form_period': form,
                                            'Incometotal': Incometotal,
                                            'CollectSum': CollectSum})


def AgentTree(request):
    # 拿到所有agent配置    payslip 2
    agent_list = AliConfig.objects.all()
    Incometotal = 0

    form = SearchForm()

    aggregated = AliConfig.objects.all().aggregate(total=Sum('IncomeTotal'))
    CollectSum = aggregated['total']

    queryset_agent = AliConfig.objects.all()
    all_records_count = queryset_agent.count()

    json_agent = {'total': all_records_count, 'rows': []}

    for agent in queryset_agent:
        json_agent['rows'].append({
            "AgentId": agent.AgentId.AgentId if agent.AgentId else "",
            "AgentName": agent.AgentId.AgentName if agent.AgentId else "",
            "AgentUpId": agent.AgentUpId.AgentId if agent.AgentUpId else "",
            "AgentUpName": agent.AgentUpId.AgentName if agent.AgentUpId else "",
            "AgentPerc": agent.AgentPerc,
            "Agent2rdPerc": agent.Agent2rdPerc,
            "Agent3rdPerc": agent.Agent3rdPerc,
            "IncomeSelf": agent.IncomeSelf,
            "IncomeLv1": agent.IncomeLv1,
            "IncomeLv2": agent.IncomeLv2,
            "IncomeTotal": agent.IncomeTotal,
            "CalculateStatus": agent.CalculateStatus,
            "Slug": '<a href="/payslip/%s">Click me</a>' % agent.Slug,

            #                 <td align="right"><a href="/payslip/{{ AliConfig.Slug }}">点我查看明细</a></td>
        })
    #     json_agent =  serializers.serialize('json', AliConfig.objects.all())

    return_dict = {'json_agent': json.dumps(json_agent, cls=DecimalEncoder),
                   'form_period': form,
                   'Incometotal': Incometotal,
                   'CollectSum': CollectSum}

    return render(request, "agent_payslip.html", return_dict)


def AgentDetail(request, agent_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        current_agent = AliConfig.objects.get(Slug=agent_name_slug)
        context_dict['agent_name'] = current_agent.AgentId.AgentName + current_agent.AgentId.AgentId

        start = request.session.get('start')
        end = request.session.get('end')

        start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(end, "%Y-%m-%d").date()

        # 1.当前代理佣金明细
        # settle date 订单结算时间
        agent_orders = AliOrd.objects.filter(PosID=current_agent.AgentId.AgentId, SettleDate__range=(start, end))
        # agent_orders = AliOrd.objects.filter(PosID=current_agent.AgentId.AgentId,CreatDate__contains=datetime.date(2017,5,15))   CreatDate__contains=end
        # agent_orders = AliOrd.objects.all()

        context_dict['agent_orders'] = agent_orders
        context_dict['current_agent'] = current_agent

        # 2.所有下线佣金明细
        agent_orders_2 = AliOrd.objects.filter(UplineId=current_agent.AgentId.AgentId,
                                               SettleDate__range=(start, end)).order_by('PosID')
        context_dict['agent_orders_2'] = agent_orders_2

        # 3.所有下下线佣金明细
        agent_orders_3 = AliOrd.objects.filter(Up2lineId=current_agent.AgentId.AgentId,
                                               SettleDate__range=(start, end)).order_by('PosID')
        context_dict['agent_orders_3'] = agent_orders_3

    except AliConfig.DoesNotExist:
        # We get here if we didn't find the specified order.
        # Don't do anything - the template displays the "no order" message for us.
        pass

    if (request.method == "POST") and ('download_statement' in request.POST):
        # style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
        #                  num_format_str='#,##0.00')
        # style1 = xlwt.easyxf(num_format_str='#')

        wb = xlwt.Workbook()
        ws = wb.add_sheet('当前代理佣金明细' + context_dict['agent_name'])
        excel_add_sheet(ws, context_dict['agent_orders'])

        ws = wb.add_sheet('所有一级下线订单')
        excel_add_sheet(ws, context_dict['agent_orders_2'])

        ws = wb.add_sheet('所有二级下线订单')
        excel_add_sheet(ws, context_dict['agent_orders_3'])

        response = HttpResponse(content_type='application/msexcel')
        response['Content-Disposition'] = 'attachment; filename=example.xls'
        wb.save(response)
        return response

        # Go render the response and return it to the client.
    return render(request, 'order.html', context_dict)


def CalculateOrderAgent(agent, start, end):
    agent_pid = agent.AgentId.AgentId
    orders = AliOrd.objects.filter(PosID=agent_pid, SettleDate__range=(start, end))

    l_UplineId = None
    l_UplineName = None
    l_Up2lineId = None
    l_Up2lineName = None

    if not agent.AgentUpId == None:
        l_UplineId = str(agent.AgentUpId.AgentId)  # 上线ID
        l_UplineName = agent.AgentUpId.AgentName  # 上线名称

        if not agent.AgentUpId.AId.AgentUpId == None:
            l_Up2lineId = str(agent.AgentUpId.AId.AgentUpId.AgentId)  # 上上线ID
            l_Up2lineName = agent.AgentUpId.AId.AgentUpId.AgentName  # 上上线名称

    AliOrd.objects.filter(PosID=agent_pid, SettleDate__range=(start, end)).update(UplineId=l_UplineId,
                                                                                  UplineName=l_UplineName,
                                                                                  Up2lineId=l_Up2lineId,
                                                                                  Up2lineName=l_Up2lineName,
                                                                                  IncomePercSelf=agent.AgentPerc,
                                                                                  SharePercUp1=agent.Agent2rdPerc,
                                                                                  SharePercUp2=agent.Agent3rdPerc)


@transaction.atomic
def CalculateOrderAmount(agent, start, end):
    # get aggent orders
    agent_pid = agent.AgentId.AgentId
    orders = AliOrd.objects.filter(PosID=agent_pid, SettleDate__range=(start, end))

    for order_item in orders:
        update_flag = False

        l_temp = round(order_item.RebateAmt * agent.AgentPerc, 2)
        if not order_item.IncomeSelf == l_temp:
            update_flag = True
            order_item.IncomeSelf = l_temp

        l_temp = round(order_item.IncomeSelf * agent.Agent2rdPerc, 2)
        if not order_item.ShareUp1 == l_temp:
            update_flag = True
            order_item.ShareUp1 = l_temp

        l_temp = round(order_item.IncomeSelf * agent.Agent3rdPerc, 2)
        if not order_item.ShareUp2 == l_temp:
            update_flag = True
            order_item.ShareUp2 = l_temp

        #                 order_item.IncomeSelf = order_item.RebateAmt * agent.AgentPerc    #自获佣金
        #                 order_item.ShareUp1 = order_item.RebateAmt * agent.Agent2rdPerc       #贡献上级佣金
        #                 order_item.ShareUp2 = order_item.RebateAmt * agent.Agent3rdPerc     #贡献上上级佣金
        if update_flag == True:
            order_item.save(update_fields=['IncomeSelf', 'ShareUp1', 'ShareUp2'])


def CalculateIncome(agent, start, end):
    agent_pid = agent.AgentId.AgentId

    # 个人订单收入
    aggregated1 = AliOrd.objects.filter(PosID=agent_pid, SettleDate__range=(start, end)).aggregate(
        Income=Sum('RebateAmt'))
    if aggregated1['Income'] == None:
        agent.IncomeSelf = 0
    else:
        agent.IncomeSelf = aggregated1['Income'] * agent.AgentPerc

    # 一级下线贡献佣金
    aggregatedLv1 = AliOrd.objects.filter(UplineId=agent_pid, SettleDate__range=(start, end)).aggregate(
        IncomeLv1=Sum('ShareUp1'))
    if aggregatedLv1['IncomeLv1'] == None:
        agent.IncomeLv1 = 0
    else:
        agent.IncomeLv1 = aggregatedLv1['IncomeLv1']
        # agent.IncomeLv1 = aggregatedLv1['IncomeLv1'] * agent.Agent2rdPerc

    # 二级下线贡献佣金
    aggregatedLv2 = AliOrd.objects.filter(Up2lineId=agent_pid, SettleDate__range=(start, end)).aggregate(
        IncomeLv2=Sum('ShareUp2'))
    if aggregatedLv2['IncomeLv2'] == None:
        agent.IncomeLv2 = 0
    else:
        agent.IncomeLv2 = aggregatedLv2['IncomeLv2']
        # agent.IncomeLv2 = aggregatedLv2['IncomeLv2'] * agent.Agent3rdPerc

    # 总佣金
    agent.IncomeTotal = agent.IncomeSelf + agent.IncomeLv1 + agent.IncomeLv2

    # 保存计算结果
    agent.save()


def save_pay_result(agent, start, end):
    if not start == None:
        year  = start.strftime('%Y')
        month = start.strftime('%m')

        updatedict={'AgentId':        agent.AgentId.AgentId if agent.AgentId else "",
                    'AgentName':      agent.AgentId.AgentName if agent.AgentId else "",
                    'AgentUpId':      agent.AgentUpId.AgentId if agent.AgentUpId else "",
                    'AgentUpName':    agent.AgentUpId.AgentName if agent.AgentUpId else "",
                    'AgentPerc':      agent.AgentPerc,
                    'Agent2rdPerc':   agent.Agent2rdPerc,
                    'Agent3rdPerc':   agent.Agent3rdPerc,
                    'ZhaohuoPid':     agent.ZhaohuoPid,
                    'ZhaohuoName':    agent.ZhaohuoName,
                    'ZhaohuoPerc':    agent.ZhaohuoPerc,
                    'ZhaohuoBot':     agent.ZhaohuoBot,
                    'GroupId':        agent.GroupId,
                    'IncomeSelf':     agent.IncomeSelf,
                    'IncomeLv1':      agent.IncomeLv1,
                    'IncomeLv2':      agent.IncomeLv2,
                    'IncomeTotal':    agent.IncomeTotal,
                    'CalculateStatus': 'OK',
                    'CalculateYear':  year,
                    'CalculateMonth': month}

        PayResult.objects.update_or_create(
            AgentId=agent.AgentId.AgentId, CalculateYear=year, CalculateMonth=month,
            defaults=updatedict)


def excel_add_sheet(ws, context_dict):
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
                         num_format_str='#,##0.00')
    line_0 = [u'淘宝订单号', u'订单创建时间', u'订单结算时间', u'商品信息', u'商品类目', u'商品数量', u'商品单价',
              u'订单状态', u'订单类型', u'付款金额', u'代理ID', u'代理', u'代理上线ID', u'代理上线', u'佣金金额']
    # 生成第一行
    for i in range(0, len(line_0)):
        ws.write(0, i, line_0[i], style0)
    line_num = 1
    for line in context_dict:
        ws.write(line_num, 0, line.OrderId)
        ws.write(line_num, 1, line.CreatDate)
        ws.write(line_num, 2, line.SettleDate)
        ws.write(line_num, 3, line.CommType)
        ws.write(line_num, 4, line.Category)
        ws.write(line_num, 5, line.CommQty)
        ws.write(line_num, 6, line.CommPrice)
        ws.write(line_num, 7, line.OrdStatus)
        ws.write(line_num, 8, line.OrdType)
        ws.write(line_num, 9, line.PayAmount)
        ws.write(line_num, 10, line.PosID)
        ws.write(line_num, 11, line.PosName)
        ws.write(line_num, 12, line.UplineId)
        ws.write(line_num, 13, line.UplineName)
        ws.write(line_num, 14, line.IncomeSelf)

        line_num = line_num + 1