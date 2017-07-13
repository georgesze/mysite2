# from django.shortcuts import render
# #from django.http import HttpResponse

# # Create your views here22

# def register(request):
    # return render(request, 'register.html')
	
	
from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField()
    headImg = forms.FileField()

def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            return HttpResponse('upload ok!')
    else:
        uf = UserForm()
    return render_to_response('register.html',{'uf':uf})