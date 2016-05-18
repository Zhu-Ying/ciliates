# -*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.

from .models import *

class BlastAdmin(admin.ModelAdmin):
    list_display=("id", "tool", 'database')
admin.site.register(Blast, BlastAdmin)