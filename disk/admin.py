from django.contrib import admin

# Register your models here.
from disk.models import AliOrd
from disk.models import AliConfig

admin.site.register(AliOrd)
admin.site.register(AliConfig)