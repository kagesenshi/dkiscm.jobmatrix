from five import grok
from plone.directives import dexterity, form
from dkiscm.jobmatrix.content.job import IJob

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IJob)
    grok.require('zope2.View')
    grok.template('job_view')
    grok.name('view')

