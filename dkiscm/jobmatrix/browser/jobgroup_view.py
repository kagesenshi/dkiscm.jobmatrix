from five import grok
from plone.directives import dexterity, form
from dkiscm.jobmatrix.content.jobgroup import IJobGroup

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IJobGroup)
    grok.require('zope2.View')
    grok.template('jobgroup_view')
    grok.name('view')

