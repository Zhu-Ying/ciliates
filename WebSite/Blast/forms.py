#coding=utf-8
from django import forms
from django.forms import ModelForm
from django.db.models import Q
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
#from django.template import loader,Context,RequestContext
#from django.http import HttpResponse,HttpResponseRedirect,Http404
import time, os
import WebSite.settings
from .models import *


class BlastForm(forms.ModelForm):
    class Meta:
        model= Blast
        fields = '__all__'
        widgets = {
            
        }
    query = forms.CharField(
        required=False,
        label='query',
        widget = forms.Textarea(attrs={"placeholder":"enter the sequence with fasta format"})    
    )
    def clean_query(self):
        if not self.cleaned_data.get('query_file'):
            query = self.cleaned_data.get('query','').replace('\r','')
            if query:
                query_file = "%s/blast/query.%d.fa" % (WebSite.settings.MEDIA_ROOT,int(time.time()))
                handle = open(query_file,'w')
                handle.write(query)
                handle.close()
                return "blast/%s" % (os.path.basename(query_file))
            else:
                raise forms.ValidationError("the query box and file do not allow empty at the same time!")
        return None
    def newsave(self):
        query = self.cleaned_data.get('query')
        blast = self.save()
        if query:
            blast.query_file = query
            blast.save()
        return blast



                

    

