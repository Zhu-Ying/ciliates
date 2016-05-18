#coding=utf-8
from django import forms
from django.forms import ModelForm
from django.db.models import Q
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time, os
import WebSite.settings
from .models import *

class SearchForm(forms.Form):
    query = forms.CharField(
        label = 'search',
        required = True
    )
    def __search_assembly(self, query, species=None):
        assemblys = Assembly.objects.filter(Q(scaffold__icontains=query) | Q(description__icontains=query))
        return assemblys.filter(species=species) if species else assemblys
    def __search_gene(self, query, species=None):
        genes = Gene.objects.filter(Q(name__icontains=query) | Q(alias__icontains=query) | Q(blast_anno__icontains=query))
        return genes.filter(assembly__species=species) if species else genes
    def __search_annotation(self, query, species=None):
        annotations = Annotation.objects.filter(
            Q(source__icontains=query) | 
            Q(feature__icontains=query) | 
            Q(description__icontains=query) |
            Q(interproscan__code__icontains=query) | 
            Q(interproscan__GO__icontains=query) | 
            Q(interproscan__description__icontains=query)
        )
        return annotations.filter(gene__assembly__species=species) if species else annotations
    def __search_blog(self, query, species=None):
        blogs = Blog.objects.filter(content__icontains=query)
        return blogs.filter(species=species) if species else blogs
    def __search_news(self, query, species=None):
        newses = News.objects.filter(Q(title__icontains=query) | Q(abstract__icontains=query))
        return newses.filter(species=species) if species else newses
    def save(self, species=None):
        query = self.cleaned_data.get('query')
        return {
            'assemblys':self.__search_assembly(query,species).count(),
            'genes':self.__search_gene(query,species).count(),
            'annotations':self.__search_annotation(query,species).count(),
            'blogs':self.__search_blog(query,species).count(),
            'newses':self.__search_news(query,species).filter(type='news').count(),
            'publications':self.__search_news(query,species).filter(type='publ').count(),
        }
    def search_list(self, type_, page=1, species=None):
        query = self.cleaned_data.get('query')
        if type_ == "assembly":
            list_ =  self.__search_assembly(query,species)
        elif type_ == "gene":
            list_ = self.__search_gene(query,species)
        elif type_ == "annotation":
            list_ = self.__search_annotation(query,species)
        elif type_ == "blogs":
            list_ = self.__search_blog(query,species)
        elif type_ == "news":
            list_ = self.__search_news(query,species).filter(type='news')
        elif type_ == "publ":
            list_ = self.__search_news(query,species).filter(type='publ')
        else:
            list_ = []
        return Paginator(list_, 20).page(page)

class JBbrowseForm(forms.Form):
    def __init__(self, species, *args, **kwargs):
        super(JBbrowseForm, self).__init__(*args, **kwargs)
        self.species = species
    query = forms.CharField(
        label = 'search',
        required = True
    )
    def clean_query(self):
        query = self.cleaned_data.get('query')
        try:
            assembly = Assembly.objects.filter(species=self.species).get(scaffold=query)
        except:
            try:
                gene = Gene.objects.filter(assembly__species=self.species).get(Q(name=query) | Q(alias=query))
            except:
                raise forms.ValidationError("please enter the exact gene name or scaffold name!")
            else:
                return "%s:%d..%d" % (gene.assembly.scaffold, gene.start, gene.end)    
        else:
            return "%s:%d..%d" % (assembly.scaffold, 1, assembly.length)
    def save(self):
        query = self.cleaned_data.get('query')
        return "/jbrowse/index.html?data=sample/json/%s&loc=%s" % (self.species.code, query)
    

