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

from arrears.models import D072Qf 
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
    WorkList.append(D072Qf(acct_month=row[0],serv_id=row[1],acc_nbr=row[2],user_name=row[3],acct_code=row[4],
                                   acct_name=row[5],product_name=row[6],current_charge=row[7],one_charge=row[8],
                                   two_charge=row[9],three_charge=row[10],four_charge=row[11],five_charge=row[12],
                                   six_charge=row[13],seven_charge=row[14],eight_charge=row[15],nine_charge=row[16],
                                   ten_charge=row[17],eleven_charge=row[18],twelve_charge=row[19],oneyear_charge=row[20],
                                   threeyear_charge=row[21],upthreeyear_charge=row[22],all_qf=row[23],morethree_qf=row[24],
                                   aging=row[25],serv_state_name=row[26],mkt_chnl_name=row[27],mkt_chnl_id=row[28],
                                   mkt_region_name=row[29],mkt_region_id=row[30],mkt_grid_name=row[31],mkt_grid_id=row[32],
                                   prod_addr=row[33]))
    n = n + 1
    if n%50000==0:
        print n
        D072Qf.objects.bulk_create(WorkList)
        WorkList = []
        time3 = time.time()
        print "读取文件耗时"+str(time2-time1)+"秒,导入数据耗时"+str(time3-time2)+"秒!"
time3 = time.time()
print n
D072Qf.objects.bulk_create(WorkList)
print "读取文件耗时"+str(time2-time1)+"秒,导入数据耗时"+str(time3-time2)+"秒!"
WorkList = []
print "成功导入数据"+str(y)+"条"
f.close() 