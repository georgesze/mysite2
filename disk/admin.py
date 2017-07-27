from django.contrib import admin

# Register your models here.
from disk.models import AliOrd,AliConfig,Agent


admin.site.register(AliOrd)
admin.site.register(AliConfig)
admin.site.register(Agent)