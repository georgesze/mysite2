from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 30)
    headImg = models.FileField(upload_to = './upload/')

    def __str__(self):
        return self.username
		
		
class Alimama(models.Model):
    order = models.CharField(max_length = 20, primary_key=True, verbose_name='订单编号')
    pid = models.CharField(max_length = 30, verbose_name='推广位')
    commission = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='结算佣金')
	
    def __str__(self):
        return self.pid
    
    class meta:
        verbose_name = "推广订单"
        verbose_name_plural = "推广订单"