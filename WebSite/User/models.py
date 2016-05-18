# -*- coding:utf-8 -*-
from django.db import models
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
# Create your models here.
#可查看信息报告，可运行软件，可编辑样本及数据信息
class Institution(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class UserInfo(models.Model):
    user = models.OneToOneField(User, related_name='User_Info')
    institution = models.ForeignKey(Institution, related_name='Institution_UserInfo')
    title = models.CharField(max_length=200)
    group = models.CharField(max_length=200, choices=(("general","普通"),("sample","样本管理"),("bioinfo","生物信息"),("report","报告签发")), default="general")
    def __str__(self):
        return self.user.username

    def checkGroup(self,permission="general"):
        #if self.user.is_superuser or self.group == 'report':
        level = {
            'general':1,
            'sample':2,
            'bioinfo':3,
            'report':4,
        }
        levelUser = 0 if self.user.is_superuser else level[self.group]
        return True if levelUser >= level[permission] else False
        
    def resetPassword(self):
        self.user.set_password("grandbox123")
        self.user.save()

def permission_required(permission):
    def _permission_required(func):
        def __permission_required(request):
            if request.user.User_Info.checkGroup(permission):
                return func(request)
            else:
                return HttpResponse("<script>alert('没有权限');history.go(-1);</script>")
        return __permission_required
    return _permission_required

def superuser_required(func):
    def _superuser_required(request):
        if request.user.is_superuser:
            return func(request)
        else:
            return HttpResponse("<script>alert('需要管理员用户权限！');history.go(-1);</script>")
    return _superuser_required



