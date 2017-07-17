from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 30)
    headImg = models.FileField(upload_to = './upload/')

    def __str__(self):
        return self.username
		
		
class Alimama(models.Model):
    pid = models.CharField(max_length = 30)
    commission = models.DecimalField(max_digits=5, decimal_places=2)
	
    def __str__(self):
        return self.pid