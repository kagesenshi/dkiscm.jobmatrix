from Acquisition import aq_inner
from zope.interface import Interface
from five import grok
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import IContentish
from plone.app.layout.viewlets import interfaces as manager
from dkiscm.jobmatrix.interfaces import IProductSpecific
from dkiscm.jobmatrix.content.job import IJob

grok.templatedir('templates')

class DownloadPDF(grok.Viewlet):
    grok.context(IJob)
    grok.viewletmanager(manager.IAboveContent)
    grok.template('downloadpdf')
    grok.layer(IProductSpecific)

    def available(self):
        return True
