#coding:utf-8 
import csv
#import os 
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www.settings") 

#import django

# if django.VERSION >= (1, 7):#自动判断版本
    # django.setup()

#from arrears.models import D072Qf 
from disk.models import AliOrd
from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile

import time
import random
from django.http.multipartparser import FILE

class UserForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()

def upld(request): 
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            #handle_uploaded_file(request.FILES['file'])         			
            # 打开文件
            #f = request.FILES['file']
            fname = request.FILES['file'].temporary_file_path()
            #myfile = csv.reader(open(fname, 'r')) 
            
            with open(fname, 'r') as f:
                reader = csv.reader(f)
                
                #print u"读取文件结束,开始导入!"
                time1 = time.time()

                WorkList = []            
            
                line_num = 0
                for line in reader: 
                    line_num = line_num + 1
                    if (line_num != 1): 
                        WorkList.append(AliOrd(CreatDate=line[0],
                                               ClickDate=line[1],
                                               CommType=line[2],
                                               CommId=line[3],
                                               WangWangId=line[4],
                                               StoreId=line[5],
                                               CommQty=line[6],
                                               CommPrice=line[7],
                                               OrdStatus=line[8],
                                               OrdType=line[9],
                                               IncomePerc=line[10],
                                               DividePerc=line[11],
                                               PayAmount=line[12],
                                               EstAmount=line[13],
                                               SettleAmt=line[14],
                                               EstIncome=line[15],
                                               SettleDate=line[16],
                                               RebatePerc=line[17],
                                               RebateAmt=line[18],
                                               AllowancePerc=line[19],
                                               AllowanceAmt=line[20],
                                               AllowanceType=line[21],
                                               Platform=line[22],
                                               ThirdParty=line[23],
                                               OrderId=line[24],
                                               Category=line[25],
                                               MediaId=line[26],
                                               MediaName=line[27],
                                               PosID=line[28],
                                               PosName=line[29]))
           
        
            #print "读取文件耗时"+str(time2-time1)+"秒,导入数据耗时"+str(time3-time2)+"秒!"
            time2    = time.time()
            #update_or_create           
            AliOrd.objects.bulk_create(WorkList)
            time3 = time.time()
            								
            return HttpResponse('upload ok!')
    else:
        uf = UserForm()
        #Person.objects.filter(age__gt=18).values_list()#括号可以指定需要的字段，一般使用这种方法。
        order_list = AliOrd.objects.all()
    return render(request, 'upld.html', {'uf':uf,
                                         'order_list':order_list})



#for row in api_data:
#    if is_new_row(row, old_data):
#        new_rows_array.append(row)
#    else:
#        if is_data_modified(row, old_data):
#            ...
#            # do the update
#        else:
#            continue
# MyModel.objects.bulk_create(new_rows_array)
