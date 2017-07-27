"""mysite2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from disk import views as main_views
from disk import upld as upld_views
from disk import search as search_views
from . import search2

urlpatterns = [
	url(r'^disk/$', main_views.register),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload/$', upld_views.upld),
    url(r'^search/$', search_views.search),
    url(r'^search-post$', search2.search_post),
]
