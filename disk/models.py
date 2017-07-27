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
    IncomePerc = models.CharField(max_length = 8, verbose_name='收入比率', default='')
    DividePerc = models.CharField(max_length = 8, verbose_name='分成比率', default='')
    PayAmount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='付款金额', default='')
    EstAmount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='预估效果', default='')
    SettleAmt = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='结算金额', default='')
    EstIncome = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='预估收入', default='')
    SettleDate = models.CharField(max_length = 20, verbose_name='结算时间', default='')
    RebatePerc = models.CharField(max_length = 8, verbose_name='佣金比例', default='')
    RebateAmt = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='佣金金额', default='')
    AllowancePerc = models.CharField(max_length = 8, verbose_name='补贴比例', default='')
    AllowanceAmt = models.CharField(max_length = 8, verbose_name='补贴金额', default='')
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
        verbose_name = '推广订单'
        verbose_name_plural = '推广订单'
            
    def __str__(self):
        return self.OrderId
    
class AliConfig(models.Model):
    class meta:
        verbose_name = "代理配置"
        verbose_name_plural = "代理配置"
          
    AgentId = models.OneToOneField('Agent', related_name='AId', default=None, blank=True, null=True)
    AgentName = models.CharField(max_length = 20, verbose_name='代理名称', default='')
    AgentUpId = models.ForeignKey('Agent', related_name='AUpId', default=None, blank=True, null=True)
    AgentUpName = models.CharField(max_length = 20, verbose_name='上线名称', blank=True)
    AgentPerc = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='自获佣金比例', default='')
    Agent2rdPerc = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='提取二级佣金比例', default='')
    Agent3rdPerc = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='提取三级佣金比例', default='')
    ZhaohuoPid = models.CharField(max_length = 20, verbose_name='找货广告位', default='', blank=True)
    ZhaohuoName = models.CharField(max_length = 20, verbose_name='找货名称', default='', blank=True)    
    ZhaohuoPerc = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='找货佣金比例', blank=True, null=True)
    ZhaohuoBot = models.CharField(max_length = 20, verbose_name='找货机器人', default='', blank=True)
    GroupId = models.CharField(max_length = 20, verbose_name='团队合伙人', default='', blank=True)
    TopLevel = models.BooleanField(verbose_name='顶级账号', default='', blank=True)
    Active = models.BooleanField(verbose_name='激活状态', default='')
    ValidBegin = models.DateField(verbose_name='有效期开始时间', blank=True, null=True)
    ValidEnd = models.DateField(verbose_name='有效期结束时间', blank=True, null=True)

    def __str__(self):
        return self.AgentId.AgentName       
    #===========================================================================
    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()
    # def approved_commentimages(self):
    #     return self.comments.filter(approved_comment=True)    
    #===========================================================================
            
    
class Agent(models.Model):
    class meta:
        verbose_name = "代理"
        verbose_name_plural = "代理"
          
    AgentId = models.CharField(max_length = 20, verbose_name=u'代理广告位', unique=True)
    AgentName = models.CharField(max_length = 20, verbose_name=u'代理名称', default='')     
    
    def __str__(self):
        return self.AgentName
    
    
       