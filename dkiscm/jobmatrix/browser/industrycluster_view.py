from five import grok
from plone.directives import dexterity, form
from dkiscm.jobmatrix.content.industrycluster import IIndustryCluster

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IIndustryCluster)
    grok.require('zope2.View')
#    grok.template('industrycluster_view')
    grok.name('view')

    def render(self):
        self.request.response.redirect(self.context.absolute_url() +
                '/folder_tabular_view')
