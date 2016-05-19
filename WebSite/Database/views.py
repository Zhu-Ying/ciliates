# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

import os,sys
from .models import *
from .forms import *
def HomeView(request):
    form = SearchForm()
    template = loader.get_template("database/home.html")
    context = RequestContext(request,{"form":form, "Species":Species.objects.all(),})
    return HttpResponse(template.render(context))
def SpeciesView(request,species_code):
    try:
        species = Species.objects.get(code=species_code)
    except Species.DoesNotExist: 
        raise Http404("error link")
    else:
        form = SearchForm()
        template = loader.get_template("database/home.html")
        context = RequestContext(request,{"species":species, "form":form, "Species":Species.objects.all(),})
        return HttpResponse(template.render(context))
def SearchView(request, species_code):
    try:
        species = Species.objects.get(code=species_code)
    except: 
        species = None
    if request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            search_result = form.save(species)
            context = RequestContext(request,{"species":species, "form":form, "search_result":search_result, "Species":Species.objects.all(),})
        else:
            context = RequestContext(request,{"species":species, "form":form})
        template = loader.get_template("database/form.html")
        return HttpResponse(template.render(context))
    else:
        raise Http404("error link")

def ListView(request):
    try:
        species = Species.objects.get(id=request.GET.get('species'))
    except:
        species = None
    page = request.GET.get('page',1)
    type_ = request.GET.get('type','unkown')
    if request.GET.get('query'):
        form = SearchForm(request.GET)
        if form.is_valid():
            paginator = form.search_list(type_=type_, page=page, species=species)
            context = RequestContext(request,{"species":species, "form":form, "paginator":paginator, "Species":Species.objects.all(),})
            template = loader.get_template("database/list.html")
            return HttpResponse(template.render(context))
    raise Http404("error link")

def GeneView(request):
    try:
        gene = Gene.objects.get(id=request.GET.get('id'))
    except Species.DoesNotExist: 
        raise Http404("error link")
    else:
        form = SearchForm()
        context = RequestContext(request,{"gene":gene, "species":gene.assembly.species, "form":form, "Species":Species.objects.all(),})
        template = loader.get_template("database/gene.html")
        return HttpResponse(template.render(context))

def GenomeView(request, species_code):
    try:
        species = Species.objects.get(code=species_code)
    except Species.DoesNotExist: 
        raise Http404("error link")
    else:
        jbrowse_url = "/jbrowse/index.html?data=sample/json/%s" % (species.code)
        if request.POST:
            form = JBbrowseForm(species, request.POST)
            if form.is_valid():
                jbrowse_url = form.save()
        else:
            form = JBbrowseForm(species)
        template = loader.get_template("database/genome.html")
        context = RequestContext(request,{"species":species, "form":form, "jbrowse_url":jbrowse_url, "Species":Species.objects.all(),})
        return HttpResponse(template.render(context))



    