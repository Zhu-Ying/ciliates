# -*- coding:utf-8 -*-

from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.http import HttpResponse,HttpResponseRedirect


from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import login_required
from  django.contrib.auth import views as userViews

from django.db.models import Count 
from django.core.servers.basehttp import FileWrapper
import os
from .models import *
from .forms import *

@login_required(login_url='/user/login')
@superuser_required
def CreateView(request, template_name= "User/create.html", template_done_name='User/create_done.html'):
    if request.POST:
        form = CreateUserForm(request.POST)
        if form.is_valid():
            request.user = form.save()
            template=loader.get_template(template_done_name)
            context=RequestContext(request,{})
            return HttpResponse(template.render(context))
    else:
        form = CreateUserForm(initial={"institution":request.user.User_Info.institution.name})
    template=loader.get_template(template_name)
    context=RequestContext(request,{'form':form,})
    return HttpResponse(template.render(context))

@login_required(login_url='/user/login')
@superuser_required
def ResetView(request, template_done_name='User/password_reset_done.html'):
    try:
        user = User.objects.get(id=request.GET.get("user"))
    except:
        return HttpResponse("<script>alert('参数错误');history.go(-1);</script>")
    else:
        user.User_Info.resetPassword()
        template=loader.get_template(template_done_name)
        context=RequestContext(request,"")
        return HttpResponse(template.render(context))

@login_required(login_url='/user/login')
@superuser_required
def UserView(request, template_name='User/users.html'):
    users = []
    for userinfo in UserInfo.objects.filter(institution=request.user.User_Info.institution):
        if not userinfo.user.is_superuser:
            users.append(userinfo.user)
    template=loader.get_template(template_name)
    context=RequestContext(request,{'users':users,})
    return HttpResponse(template.render(context))

@login_required(login_url='/user/login')
@superuser_required
def ManageView(request, template_name='User/manage.html'):
    user = User.objects.get(id=request.GET.get('user'))
    userinfo = user.User_Info
    if request.POST:
        form = ManageUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('manage?user='+str(user.id))
    else:

        form = ManageUserForm(initial={"user":user, "institution":userinfo.institution, "title":userinfo.title, "group":userinfo.group})
    template=loader.get_template(template_name)
    context=RequestContext(request,{'form':form,})
    return HttpResponse(template.render(context))

@login_required(login_url='/user/login')
@superuser_required
def Delete(request):
    try:
        UserInfo.objects.filter(user__id=request.GET.get("user")).delete()
        User.objects.filter(id=request.GET.get("user")).delete()
    except:
        return HttpResponse("false")
    else:
        return HttpResponse("true")

# Create your views here.
