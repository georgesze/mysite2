from django.contrib import admin

# Register your models here.
from disk.models import AliOrd,AliConfig,Agent

# Add in this class to customized the Admin Interface
class AliConfigAdmin(admin.ModelAdmin):
    prepopulated_fields = {'Slug':('AgentId',)}


admin.site.register(AliOrd)
admin.site.register(AliConfig,AliConfigAdmin)
admin.site.register(Agent)