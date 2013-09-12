from five import grok
from plone.directives import dexterity, form
from dkiscm.jobmatrix.content.job import IJob
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from Acquisition import aq_parent
from dkiscm.jobmatrix.content.jobgroup import IJobGroup
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


class PDFPrintView(Index):
    grok.name('pdf_print_view')
    grok.template('pdf_print_view')


class PDFExportView(grok.View):
    grok.name('pdf_export_view')
    grok.context(IJob)

    def render(self):
        html = self.context.restrictedTraverse('pdf_print_view')().encode('utf-8')
        result = StringIO()
        pdf = pisa.CreatePDF(StringIO(html), result)
        out = result.getvalue()
        self.request.response.setHeader('Content-Type', 'application/pdf')
        self.request.response.setHeader('Content-Length', len(out))
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



