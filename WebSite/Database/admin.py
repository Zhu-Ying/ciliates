# -*- coding:utf-8 -*-
from django.contrib import admin

# Register your models here.

from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display=("id", "name")
admin.site.register(Category, CategoryAdmin)

class SpeciesAdmin(admin.ModelAdmin):
    list_display=("id", "code", "name", "category")
admin.site.register(Species, SpeciesAdmin)

class AssemblyAdmin(admin.ModelAdmin):
    list_display=("id", "scaffold", "length")
admin.site.register(Assembly, AssemblyAdmin)

class GeneAdmin(admin.ModelAdmin):
    list_display=("id", "name", "alias", "assembly")
admin.site.register(Gene, GeneAdmin)

class StructAdmin(admin.ModelAdmin):
    list_display=("id", "name", "function", "gene")
admin.site.register(Struct, StructAdmin)

class TranscriptAdmin(admin.ModelAdmin):
    list_display=("id", "name", "gene")
admin.site.register(Transcript, TranscriptAdmin)

class InterproScanAdmin(admin.ModelAdmin):
    list_display=("id", "code")
admin.site.register(InterproScan, InterproScanAdmin)

class AnnotationAdmin(admin.ModelAdmin):
    list_display=("id", "source", "feature", "gene")
admin.site.register(Annotation, AnnotationAdmin)

class DataAdmin(admin.ModelAdmin):
    list_display=("id", "species")
admin.site.register(Data, DataAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display=("id", "type", "species")
admin.site.register(Blog, BlogAdmin)

class NewsAdmin(admin.ModelAdmin):
    list_display=("id", "type", "title", "date", "species")
admin.site.register(News, NewsAdmin)
