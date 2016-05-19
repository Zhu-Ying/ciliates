# -*- coding:utf-8 -*-
from django.conf.urls import include, url, patterns
from .views import *
urlpatterns = patterns('',
    url(r'^home$', HomeView),
    url(r'^species/(\w{2})$', SpeciesView),
    url(r'^search/(\w*)$', SearchView),
    url(r'^list$', ListView),
    url(r'^gene$', GeneView),
    url(r'^genome/(\w{2})$', GenomeView),
)