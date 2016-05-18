#coding=utf-8
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group

import time, os, re
from .models import *


class CreateUserForm(forms.Form):
    username = forms.CharField(
        max_length = 200,
        required = True,
        label = '用户',
    )
    password = forms.CharField(
        max_length = 200,
        required = True,
        label = '密码',
        widget = forms.PasswordInput(),
    )
    confirm = forms.CharField(
        max_length = 200, 
        required = True, 
        label = "确认",
        widget = forms.PasswordInput(),
    )
    email = forms.EmailField(
        required = True, 
        label = "邮箱",
        widget = forms.EmailInput()
    )
    institution = forms.CharField(
        max_length = 200,
        required = True,
        label = '机构',
        widget = forms.TextInput(attrs={"readonly":"readonly"})
    )
    title = forms.CharField(
        max_length=200,
        required = True,
        label = '职位',
    )
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username = username)
        except:
            if re.search(r'^\w+$', username):
                return username
            else:
                raise forms.ValidationError('用户名由“数字”、“字母”、“下划线”组成')
        else:
            raise forms.ValidationError('该用户名已经存在')

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError('密码长度必须大于6')
        else:
            return password

    def clean_confirm(self):
        password = self.cleaned_data['password'] if 'password' in self.cleaned_data else ""
        confirm = self.cleaned_data['confirm']
        if password == confirm:
            return confirm
        else:
            raise forms.ValidationError('两次输入密码不匹配')
    def clean_institution(self):
        institutionName = self.cleaned_data['institution']
        try:
            institution = Institution.objects.get(name=institutionName)
        except:
            institution = Institution(name=institutionName)
            institution.save()
        return institution
        
    def save(self):
       username = self.cleaned_data['username']
       password = self.cleaned_data['password']
       email = self.cleaned_data['email']
       institution = self.cleaned_data['institution']
       title = self.cleaned_data['title']
       user = User.objects.create_user(username, email, password)
       user.save()
       userInfo = UserInfo(user=user, institution=institution, title=title)
       userInfo.save()
       return user

class ManageUserForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset = User.objects.all(), 
        required = True, 
        label = "用户",
        widget = forms.Select(attrs={'readonly':'readonly'}),
    )
    institution = forms.CharField(
        max_length = 200,
        required = True,
        label = '机构',
    )
    title = forms.CharField(
        max_length=200,
        required = True,
        label = '职位',
    )
    group = forms.ChoiceField(
        choices=(("general","普通"),("sample","样本管理"),("bioinfo","生物信息"),("report","报告签发")),
        required = True,
        label = '用户组',
        widget = forms.RadioSelect()
    )
    def clean_institution(self):
        institutionName = self.cleaned_data['institution']
        try:
            institution = Institution.objects.get(name=institutionName)
        except:
            institution = Institution(name=institutionName)
            institution.save()
        return institution
    def save(self):
       user = self.cleaned_data['user']
       institution = self.cleaned_data['institution']
       title = self.cleaned_data['title']
       group = self.cleaned_data['group']
       user.User_Info.institution = institution
       user.User_Info.title = title
       user.User_Info.group = group
       user.User_Info.save()
       return user