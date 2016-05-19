# -*- coding:utf-8 -*-
from django.conf.urls import include, url, patterns
from .views import *
urlpatterns = patterns('',
    url(r'^home$', BlastHomeView),
    url(r'^species/(\w{2})$', BlastSpeciesView),
    url(r'^result/(\w+)$', ResultView),
    
)