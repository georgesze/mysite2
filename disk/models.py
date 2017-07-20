from django.db import models
from django.template.defaultfilters import default
from django.forms.widgets import Media

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 30)
    headImg = models.FileField(upload_to = './upload/')

    def __str__(self):
        return self.username
		
		                          #primary_key=True, 
class AliOrd(models.Model):
    CreatDate = models.DateTimeField(verbose_name='创建时间', default='')
    ClickDate = models.DateTimeField(verbose_name='点击时间', default='')
    CommType = models.CharField(max_length = 20, verbose_name='商品信息', default='')
    CommId = models.CharField(max_length = 20, verbose_name='商品ID', default='')
    WangWangId = models.CharField(max_length = 20, verbose_name='掌柜旺旺', default='')
    StoreId = models.CharField(max_length = 20, verbose_name='所属店铺', default='')
    CommQty = models.CharField(max_length = 20, verbose_name='商品数', default='')
    CommPrice = models.CharField(max_length = 20, verbose_name='商品单价', default='')
    OrdStatus = models.CharField(max_length = 20, verbose_name='订单状态', default='')
    OrdType = models.CharField(max_length = 20, verbose_name='订单类型', default='')
    IncomePerc = models.CharField(max_length = 20, verbose_name='收入比率', default='')
    DividePerc = models.CharField(max_length = 20, verbose_name='分成比率', default='')
    PayAmount = models.CharField(max_length = 20, verbose_name='付款金额', default='')
    EstAmount = models.CharField(max_length = 20, verbose_name='预估效果', default='')
    SettleAmt = models.CharField(max_length = 20, verbose_name='结算金额', default='')
    EstIncome = models.CharField(max_length = 20, verbose_name='预估收入', default='')
    SettleDate = models.CharField(max_length = 20, verbose_name='结算时间', default='')
    RebatePerc = models.CharField(max_length = 20, verbose_name='佣金比例', default='')
    RebateAmt = models.CharField(max_length = 20, verbose_name='佣金金额', default='')
    AllowancePerc = models.CharField(max_length = 20, verbose_name='补贴比例', default='')
    AllowanceAmt = models.CharField(max_length = 20, verbose_name='补贴金额', default='')
    AllowanceType = models.CharField(max_length = 20, verbose_name='补贴类型', default='')
    Platform = models.CharField(max_length = 20, verbose_name='成交平台', default='')
    ThirdParty = models.CharField(max_length = 20, verbose_name='第三方服务', default='')
    OrderId = models.CharField(max_length = 20, verbose_name='订单编号', default='')
    Category = models.CharField(max_length = 20, verbose_name='类目名称', default='')
    MediaId = models.CharField(max_length = 20, verbose_name='来源媒体ID', default='')
    MediaName = models.CharField(max_length = 20, verbose_name='来源媒体名称', default='')
    PosID = models.CharField(max_length = 20, verbose_name='广告位ID', default='')
    PosName = models.CharField(max_length = 20, verbose_name='广告位名称', default='')
    
	
    class meta:
        verbose_name = "推广订单"
        verbose_name_plural = "推广订单"
            
    
    def __str__(self):
        return self.OrderId
    
        
        