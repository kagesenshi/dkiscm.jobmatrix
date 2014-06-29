from five import grok
from plone.directives import dexterity, form
from dkiscm.jobmatrix.content.job import IJob
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from Acquisition import aq_parent
from dkiscm.jobmatrix.content.jobgroup import IJobGroup
from dkiscm.jobmatrix.content.industrycluster import IIndustryCluster
from Products.CMFCore.interfaces import ISiteRoot
import xhtml2pdf.pisa as pisa
from StringIO import StringIO

from pyPdf import PdfFileWriter, PdfFileReader

import logging
logger = logging.getLogger('dkiscm.jobmatrix')

def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in
        range(input.numPages)]

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IJob)
    grok.require('zope2.View')
    grok.template('job_view')
    grok.name('view')


    def cluster_title(self):
        cluster = aq_parent(aq_parent(self.context))
        return cluster.title

    def cluster(self):
        group = aq_parent(self.context)
        if not IJobGroup.providedBy(group):
            return None
        cluster = aq_parent(group)
        if not IIndustryCluster.providedBy(cluster):
            return None
        return cluster

    def industry_experience(self):
        vocab = getUtility(
            IVocabularyFactory,
            name='dkiscm.jobmatrix.experienceyears'
        )(self.context)

        result = []
        levels = [i.value for i in self.exp_levels()]
        return [i for i in vocab if i.value in levels]

    def job_grouping(self):
        parent = aq_parent(self.context)
        if not IJobGroup.providedBy(parent):
            return []

        parent_container = aq_parent(parent)
        groups = []
        for o in parent_container.values():
            if IJobGroup.providedBy(o):
                data = {
                    'title': o.pretty_title_or_id(),
                    'css_class': ''
                }
                if o == parent:
                    data['css_class'] = 'selected-group'
                groups.append(data)
        return groups

    def education(self):
        selected = self.context.education
        vocab = getUtility(IVocabularyFactory,
                name='dkiscm.jobmatrix.education')(self.context)
        result = []
        for term in vocab:
            data = {
                'title': term.title,
                'css_class': ''
            }

            if term.value == selected:
                data['css_class'] = 'selected-education'

            result.append(data)

        return result

    def exp_levels(self):
        vocab = getUtility(IVocabularyFactory,
            name='dkiscm.jobmatrix.experience')(self.context)
#        result = []
#        for exp in (self.context.exp_levels or []):
#            result.append(vocab.getTerm(exp))
        return [term for term in vocab]

    def softskills_competency_columns(self):
        competencies = self.context.softskills_competency
        cols = {}
        for c in competencies:
            for col in c:
                cols.setdefault(col, [])
                if c[col]:
                    cols[col].append(c[col])
        return sorted([c for c in cols if ('col' in c)])

    def get_technical_skill_cell_class(self, item, experience):
        if item['%s_required' % experience.value]:
            return 'required-cell'
        if experience.value in self.context.exp_levels:
            return 'normal-cell'
        return 'blank-cell'

    def cluster_css(self):
        cluster = self.cluster()
        return u'''
        .cluster-infobox {
            background: %(infobox_bgcolor)s !important;
        }

        .dkiscm-job-heading {                                                   
            border-bottom: 3px solid #000000 !important;                        
        }                                                                       
        .job-heading {                                                          
            color: white !important;                                            
            padding-left: 5px !important;                                       
        }                                                                       
        .dkiscm-jobcluster-color {                                              
            color: %(infobox_bgcolor)s !important;                              
        }

        .dkiscm-skilltable th {
            background: %(th_bgcolor)s !important;
        }

        .normal-cell {
            background: %(td_bgcolor)s !important;
        }

        .required-cell {
            background: %(highlighted_td_bgcolor)s !important;
        }

        .dkiscm-description-column {
            background: %(heading_td_bgcolor)s !important;
        }

        .descriptioncolumn {
            background: %(heading_td_bgcolor)s !important;
        }

        .counter-cell {
            background: %(heading_td_bgcolor)s !important;
        }

        .weight-cell-1 {
            background: %(weight1_bgcolor)s !important;
        }
        
        .weight-cell-2 {
            background: %(weight2_bgcolor)s !important;
        }
        
        .weight-cell-3 {
            background: %(weight3_bgcolor)s !important;
        }
        
        .weight-cell-4 {
            background: %(weight4_bgcolor)s !important;
        }
        
        .weight-cell-5 {
            background: %(weight5_bgcolor)s !important;
        }

        ''' % {
            'infobox_bgcolor': cluster.infobox_bgcolor,
            'th_bgcolor': cluster.th_bgcolor,
            'td_bgcolor': cluster.td_bgcolor,
            'highlighted_td_bgcolor': cluster.highlighted_td_bgcolor,
            'heading_td_bgcolor': cluster.heading_td_bgcolor,
            'weight1_bgcolor': cluster.weight1_bgcolor,
            'weight2_bgcolor': cluster.weight2_bgcolor,
            'weight3_bgcolor': cluster.weight3_bgcolor,
            'weight4_bgcolor': cluster.weight4_bgcolor,
            'weight5_bgcolor': cluster.weight5_bgcolor
        }


    def job_demand(self):
        if self.context.job_demand_synovate2013 <= 15:
            return 'low'
        if self.context.job_demand_synovate2013 <= 150:
            return 'medium'
        if self.context.job_demand_synovate2013 > 150:
            return 'high'
        return 'low'

    def certification_colspan(self):
        available_levels = [i.value for i in self.exp_levels()]
        left = 0
        def sortkey(x):
            return available_levels.index(x)

        sorted_levels = sorted(
            self.context.exp_levels, key=sortkey
        )
        for i in available_levels:
            if sorted_levels[0] == i:
                break
            left += 1
        center = len(self.context.exp_levels)
        right = 5 - left - center
        return {
            'left': left, 
            'center': center, 
            'right': right
        }


class PDFPrintView(Index):
    grok.name('pdf_print_view')
    grok.template('pdf_print_view')

    def pagebreak(self):
        if self.request.get('nopagebreak', False):
            return False
        return True

    def pdfonly_cluster_css(self):
        cluster = self.cluster()

        return u'''
        th {
                    background: %(th_bgcolor)s !important;
        }

        .dkiscm-job-information {                                                                                     
            padding-top: 0px !important;                                        
            margin-bottom: 0px !important;                                      
        }
        
        .skilltable {                                                           
            padding: 0px !important;                                            
        }
        ''' % {
            'infobox_bgcolor': cluster.infobox_bgcolor,
            'th_bgcolor': cluster.th_bgcolor,
            'td_bgcolor': cluster.td_bgcolor,
            'highlighted_td_bgcolor': cluster.highlighted_td_bgcolor,
            'heading_td_bgcolor': cluster.heading_td_bgcolor,
            'weight1_bgcolor': cluster.weight1_bgcolor,
            'weight2_bgcolor': cluster.weight2_bgcolor,
            'weight3_bgcolor': cluster.weight3_bgcolor,
            'weight4_bgcolor': cluster.weight4_bgcolor,
            'weight5_bgcolor': cluster.weight5_bgcolor
        }



class PDFExportView(grok.View):
    grok.name('pdf_view')
    grok.context(IJob)

    def render(self):
        result = self._render_pdf()
        pdfreader = PdfFileReader(result)
        if pdfreader.getNumPages() > 2:
            result = self._render_nopagebreak()
        out = result.getvalue()
        self.request.response.setHeader('Content-Type', 'application/pdf')
        self.request.response.setHeader('Content-Length', len(out))
        return out

    def _render_pdf(self):
        html = self.context.restrictedTraverse('pdf_print_view')().encode('utf-8')
        result = StringIO()
        pdf = pisa.CreatePDF(StringIO(html), result)
        return result

    def _render_nopagebreak(self):
        self.request.set('nopagebreak', True)
        return self._render_pdf()




class PDFDownload(PDFExportView):
    grok.name('pdf_download')
    grok.context(IJob)

    def render(self):
        out = super(PDFDownload, self).render()
        filename = '%s_%s' % (self.context.getId().upper(),
                self.context.Title().replace(' ', '_'))
        self.request.response.setHeader('Content-Disposition',
                            'attachment; filename=%s.pdf' %
                            filename)
        return out



class ExportAllView(grok.View):
    grok.name('pdf_export_all')
    grok.context(ISiteRoot)

    def render(self):
        pdfoutput = PdfFileWriter()

        for brain in self.context.portal_catalog({
            'portal_type':'dkiscm.jobmatrix.job'
            }):
            obj = brain.getObject()
            html = obj.restrictedTraverse('pdf_print_view')()
            result = StringIO()

            try:
                pdf = pisa.CreatePDF(StringIO(html), result)
            except:
                logger.error('Unable to convert job to PDF : %s' % obj.absolute_url())
                continue
            append_pdf(PdfFileReader(result), pdfoutput)

        output = StringIO()
        pdfoutput.write(output)

        out = output.getvalue()

        self.request.response.setHeader('Content-Type', 'application/pdf')
        self.request.response.setHeader('Content-Length', len(out))
        return out



