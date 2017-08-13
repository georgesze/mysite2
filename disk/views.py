#coding:utf-8 
# from django.shortcuts import render
# #from django.http import HttpResponse

# # Create your views here22

# def register(request):
    # return render(request, 'register.html')
	
	
from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from disk.models import User

# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField()
    headImg = forms.FileField()

def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
		
            # get form information
            username = uf.cleaned_data['username']
            headImg = uf.cleaned_data['headImg']
			# write to database
            user = User()
            user.username = username
            user.headImg = headImg
            user.save()
            return HttpResponse('upload ok!')
    else:
        uf = UserForm()
    #return render_to_response('register.html',{'uf':uf})
    return render(request, 'register.html', {'uf':uf})


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am the KING of the world --- by George.Shi"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'index.html', context_dict)