# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

import os,sys
from Database import models as DatabaseModels
from Database import forms as DatabaseForms
from .models import *
from .forms import *

def BlastSpeciesView(request,species_code):
    try:
        species = DatabaseModels.Species.objects.get(code=species_code)
        data = DatabaseModels.Data.objects.get(species=species)
    except DatabaseModels.Species.DoesNotExist: 
        raise Http404("error link")
    else:
        if request.POST:
            blastform = BlastForm(request.POST, request.FILES)
            if blastform.is_valid():

                blast = blastform.newsave()
                #blast.run()
                return HttpResponseRedirect('/blast/result?id='+str(blast.id))
        else:
            blastform = BlastForm(
                initial={
                    'database':data,                    
                }
            )
        context = RequestContext(request,{"species":species, "blastform":blastform, "form":DatabaseForms.SearchForm()})
        template = loader.get_template("blast/form.html")
        return HttpResponse(template.render(context))

        
