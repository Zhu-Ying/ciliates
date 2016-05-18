from django.contrib import admin

# Register your models here.

from .models import *

class InstitutionAdmin(admin.ModelAdmin):
    list_display=("id","name")
admin.site.register(Institution,InstitutionAdmin)

class UserInfoAdmin(admin.ModelAdmin):
    list_display=("id","user","group","institution","title")
admin.site.register(UserInfo,UserInfoAdmin)
