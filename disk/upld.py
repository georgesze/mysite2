#coding:utf-8 

import os 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www.settings") 

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''
import django

if django.VERSION >= (1, 7):#自动判断版本
    django.setup()

#from arrears.models import D072Qf 
from disk.models import Alimama
import time
import random
time1 = time.time()
f = open('11.csv')
print u"读取文件结束,开始导入!"
time2 = time.time()
WorkList = []
next(f) #将文件标记移到下一行
y = 0
n = 1
for line in f:
    row = line.replace('"','') #将字典中的"替换空
    row = row.split(';') #按;对字符串进行切片
    y = y + 1
    WorkList.append(Alimama(pid=row[0],commission=row[1]))
	
    n = n + 1
    if n%50000==0:
        print n
        Alimama.objects.bulk_create(WorkList)
        WorkList = []
        time3 = time.time()
        print "读取文件耗时"+str(time2-time1)+"秒,导入数据耗时"+str(time3-time2)+"秒!"
time3 = time.time()
print n
Alimama.objects.bulk_create(WorkList)
print "读取文件耗时"+str(time2-time1)+"秒,导入数据耗时"+str(time3-time2)+"秒!"
WorkList = []
print "成功导入数据"+str(y)+"条"
f.close() 