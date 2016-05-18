# -*- coding:utf-8 -*-
from django.db import models
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from ckeditor.fields import RichTextField
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='名称')
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Species(models.Model):
    code = models.CharField(max_length=200, verbose_name='代号')
    name = models.CharField(max_length=200, verbose_name='名称')
    introduction = models.TextField(verbose_name='简介')
    description = models.TextField(verbose_name='描述')
    category = models.ForeignKey(Category, verbose_name='分类', related_name='Category_Species',)
    def __str__(self):
        return self.name


class Assembly(models.Model):
    scaffold = models.CharField(max_length=200, verbose_name='名称')
    length = models.IntegerField(verbose_name='长度')
    sequence = models.TextField(verbose_name='序列')
    description = models.TextField(verbose_name='描述')
    species = models.ForeignKey(Species, verbose_name='物种', related_name='Species_Assembly')
    class Meta:
        ordering = ['scaffold',]
    def __str__(self):
        return self.scaffold

class Gene(models.Model):
    name = models.CharField(max_length=200, verbose_name='名称', db_index=True)
    alias = models.CharField(max_length=200, blank=True, verbose_name='别名', db_index=True)
    start = models.IntegerField(verbose_name='scaffold中起始位置')
    end = models.IntegerField(verbose_name='scaffold中结束位置')
    is_forward = models.BooleanField(verbose_name='是否正向')
    blast_anno = models.CharField(max_length=200, blank=True, verbose_name='BLAST 注释')
    assembly = models.ForeignKey(Assembly, verbose_name='Assembly', related_name='Assembly_Gene')
    class Meta:
        ordering = ['name',]
    def __str__(self):
        return self.name
    def strand(self):
        return '+' if self.is_forward else '-'
    class Meta:
        ordering = ['name',]
    def length(self):
        return self.end-self.start+1

class Struct(models.Model):
    name = models.CharField(max_length=200, verbose_name='名称')
    function = models.CharField(max_length=200, verbose_name='功能区域', choices=(('utr','utr'),('exon','exon'),('intron','intron')))
    start = models.IntegerField(verbose_name='gene中起始位置')
    end = models.IntegerField(verbose_name='gene中结束位置')
    comment = models.CharField(max_length=200, verbose_name='其他备注')
    gene = models.ForeignKey(Gene, verbose_name='基因', related_name='Gene_Struct')
    def __str__(self):
        return '%s:%s' % (self.gene.name, self.name)
    class Meta:
        ordering = ['start',]
    def length(self):
        return self.end-self.start+1
    def percent(self):
        return 100*self.length()/self.gene.length()


class Transcript(models.Model):
    name = models.CharField(max_length=200, verbose_name='名称', db_index=True)
    expression = models.FloatField(verbose_name='表达量', null=True)
    seqNA = models.TextField(verbose_name='核酸序列')
    seqAA = models.TextField(verbose_name='氨基酸序列')
    gene = models.OneToOneField(Gene, verbose_name='基因', related_name='Gene_Transcript')
    def __str__(self):
        return self.name


class InterproScan(models.Model):
    code = models.CharField(max_length=200, verbose_name='InterproScan ID')
    GO = models.CharField(max_length=200, verbose_name='GO', blank=True)
    description = models.TextField(verbose_name='描述')
    def __str__(self):
        return self.code

class Annotation(models.Model):
    source = models.CharField(max_length=200, verbose_name='source')
    feature = models.CharField(max_length=200, verbose_name='feature')
    start = models.IntegerField(verbose_name='gene中起始位置')
    end = models.IntegerField(verbose_name='gene中结束位置')
    description = models.TextField(verbose_name='description')
    gene = models.ForeignKey(Gene, verbose_name='基因', related_name='Gene_Annotation')
    interproscan = models.ForeignKey(InterproScan, verbose_name='InterproScan', related_name='InterproScan_Annotation', null=True)
    def __str__(self):
        return self.source
    class Meta:
        ordering = ['start',]

class Data(models.Model):
    assembly = models.FileField(max_length=200, upload_to='file', blank=True, verbose_name='组装基因组文件')
    cds = models.FileField(max_length=200, upload_to='file', blank=True, verbose_name='转录本cds文件')
    protein = models.FileField(max_length=200, upload_to='file', blank=True, verbose_name='蛋白文件')
    annotation = models.FileField(max_length=200, upload_to='file', blank=True, verbose_name='注释文件')
    species = models.OneToOneField(Species,verbose_name='物种', related_name='Species_Data')
    def __str__(self):
        return self.species.name

class Blog(models.Model):
    type = models.CharField(max_length=200, verbose_name='blog类型', choices=(('taxon','TAXONOMY'),('morph','MORPHOLOGY'),('proto','PROTOCALS')))
    #content = models.TextField(verbose_name='内容')
    content = RichTextField()
    species = models.ForeignKey(Species,verbose_name='物种')
    def __str__(self):
        return "%s:%s" % (self.species.name, self.type)

class News(models.Model):
    type = models.CharField(max_length=200, verbose_name='blog类型', choices=(('news','NEWS'),('publ','PUBLICATION')))
    title = models.CharField(max_length=200, verbose_name='标题')
    abstract = models.TextField(verbose_name='摘要')
    link = models.CharField(max_length=255, verbose_name='链接')
    date = models.DateField(verbose_name='日期')
    species = models.ForeignKey(Species,verbose_name='物种', related_name='Species_News')

'''
class CLRnetworkManager(models.Manager):
    def network(self, genes):
        genes.sort()
        networks = {
            'genes':genes,
            'CLRs':[]
        }
        for gene1 in genes:
            row = []
            for gene2 in genes:
                try:
                    CLR = self.get(Q(gene1=gene) | Q(gene2=gene))
                except:
                    CLR = None
                else:
                    row.append(CLR)
            networks.CLRs.append(row)
        return network

class CLRnetwork(models.Model):
    gene1 = models.ForeignKey(Gene, verbose_name='基因1', related_name='Gene_Transcript_1')
    gene2 = models.ForeignKey(Gene, verbose_name='基因2', related_name='Gene_Transcript_2')
    value = models.FloatField(verbose_name='值')
'''
