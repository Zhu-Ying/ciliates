# -*- coding:utf-8 -*-
from django.db import models
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
import WebSite.settings, os, mimetypes, json, time
from Bio.Blast import NCBIXML
# Create your models here.

from Database import models as DatabaseModels

blast_tool_choices=(
    ('blastn', 'blastn'),
    ('tblastn', 'tblastn')
)
blast_evalue_choices=(
    (0.0001,'0.0001'),
    (0.001,'0.001'),
    (0.01, '0.01'),
    (0.1, '0.1'),
    (1, '1'),
    (10, '10'),
    (100, '100'),
    (1000, '1000')
)
blast_outfmt_choices=(
    (0, 'pairwise'),
    (1, 'query-anchored showing identities'),
    (2, 'query-anchored no identities'),
    (3, 'flat query-anchored, show identities'),
    (4, 'flat query-anchored, no identities'),
    (5, 'XML Blast output'),
    (6, 'tabular'),
    (7, 'tabular with comment lines'),
    (8, 'Text ASN.1'),
    (9, 'Binary ASN.1'),
    (10, 'Comma-separated values'),
    (11, 'BLAST archive format (ASN.1)'),
    (12, 'JSON Seqalign output')
)
class Blast(models.Model):
    query_file = models.FileField(verbose_name='query_file', blank=True, upload_to='blast/')
    database = models.ForeignKey(DatabaseModels.Data, verbose_name='Database')
    tool = models.CharField(max_length=200, verbose_name='Program', choices=blast_tool_choices, default='blastn')
    evalue = models.FloatField(verbose_name='Expect Value', choices=blast_evalue_choices, default=1)
    alignments = models.IntegerField(verbose_name='Num Alignments', default=250)
    outfmt = models.IntegerField(verbose_name='Out Format', choices=blast_outfmt_choices, default=6)
    other = models.CharField(max_length=200, blank=True, verbose_name='Other Options')
    def __str__(self):
        return "%s:%s:%s" % (self.tool, self.database.species.name, self.id)
    def subject(self):
        if self.tool in ('blastn', 'tblastn', 'tblastx'):
            return self.database.assembly.path
        else:
            return self.database.protein.path
    def outfile(self):
        return {
            "text":"%s/blast/blast.%d.out.txt" % (WebSite.settings.MEDIA_ROOT, self.id),
            "xml":"%s/blast/blast.%d.out.xml" % (WebSite.settings.MEDIA_ROOT, self.id),
        }
    def params(self):
        return (
            {"name":"tool", "value":self.tool},
            {"name":"species", "value":self.database.species.name},
            {"name":"evalue", "value":self.evalue},
            {"name":"num_alignments", "value":self.alignments},
            {"name":"other", "value":self.other}
        )
    def run(self):
        #'%s/blast/bin/%s -query %s -db %s -out %s -evalue %f -outfmt %d -num_alignments %d %s' % (WebSite.settings.SOFT_DIR, self.tool, self.query_file.path, self.subject(), self.outfile(), self.evalue, self.outfmt, self.alignments, self.other)
        command_base = '%s/blast/bin/%s -query %s -db %s -evalue %f -num_alignments %d %s' % (WebSite.settings.SOFT_DIR, self.tool, self.query_file.path, self.subject(), self.evalue, self.alignments, self.other)
        command_text = "%s -out %s -outfmt %d" % (command_base, self.outfile()['text'], self.outfmt)
        command_xml = "%s -out %s -outfmt %d" % (command_base, self.outfile()['xml'], 5)
        os.system(command_text)
        os.system(command_xml)
    def parse(self):
        outfile = self.outfile()['xml']
        if os.path.exists(outfile):
            return NCBIXML.parse(open(outfile,'r'))
        else:
            None
    def download(self):
        outfile = self.outfile()['text']
        if os.path.exists(outfile):
            wrapper = FileWrapper(open(outfile,'rb'))
            response = HttpResponse(wrapper, content_type = mimetypes.guess_type(outfile)[0])
            response['Content-Length'] = os.path.getsize(outfile)
            response['Content-Disposition'] = 'attachment; filename=%s' % (os.path.basename(outfile),)
            return response
        return None 

