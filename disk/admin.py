#coding:utf-8 
from django.contrib import admin

# Register your models here.
from disk.models import AliOrd, AliConfig, Agent, PayResult

# Add in this class to customized the Admin Interface
class AliConfigAdmin(admin.ModelAdmin):
    None
    # prepopulated_fields doesn’t accept DateTimeField, ForeignKey, OneToOneField, and ManyToManyField fields.
    #prepopulated_fields = {'Slug': ('AgentId',)}


admin.site.register(AliOrd)
admin.site.register(AliConfig, AliConfigAdmin)
admin.site.register(Agent)
admin.site.register(PayResult)