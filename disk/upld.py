#coding:utf-8 
import csv
#import os 
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www.settings") 

#import django

# if django.VERSION >= (1, 7):#自动判断版本
    # django.setup()

#from arrears.models import D072Qf 
from disk.models import Alimama
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
                        WorkList.append(Alimama(pid=line[28],commission=line[18]))
        
            #print "读取文件耗时"+str(time2-time1)+"秒,导入数据耗时"+str(time3-time2)+"秒!"
            time2    = time.time()
                       
            Alimama.objects.bulk_create(WorkList)
            time3 = time.time()
            								
            return HttpResponse('upload ok!')
    else:
        uf = UserForm()
    return render(request, 'upld.html', {'uf':uf})


