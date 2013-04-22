from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource
from Products.CMFCore.utils import getToolByName
from dkiscm.jobmatrix import MessageFactory as _
from dkiscm.jobmatrix.content.industrycluster import IIndustryCluster

class BaseVocabularyFactory(grok.GlobalUtility):
    grok.baseclass()
    grok.implements(IVocabularyFactory)
    terms = []

    def __call__(self, context):
        terms = []
        for item in self.terms:
            terms.append(SimpleTerm(**item))
        return SimpleVocabulary(terms)

class IndustryCluster(BaseVocabularyFactory):
    grok.name('dkiscm.jobmatrix.industrycluster')

    def __call__(self, context):
        results = []
        for brain in context.portal_catalog(
            object_provides=IIndustryCluster.__identifier__
            ):
            results.append({
                'value': brain.getId,
                'title': brain.Title
            })

        terms = []
        for item in results:
            terms.append(SimpleTerm(**item))
        return SimpleVocabulary(terms)




class JobGroupingVocabularyFactory(BaseVocabularyFactory):
    grok.name('dkiscm.jobmatrix.jobgrouping')

    terms = [{
        'title': 'Pre-Production',
        'value': 'preproduction'
    },{
        'title': 'Production',
        'value': 'production',
    },{
        'title': 'Post-Production',
        'value': 'postproduction'
    }]


class EducationVocabularyFactory(BaseVocabularyFactory):
    grok.name('dkiscm.jobmatrix.education')

    terms = [{
        'title': 'SPM',
        'value':'spm'
    },{
        'title': 'Certificate',
        'value': 'certificate'
    },{
        'title': 'Diploma',
        'value': 'diploma'
    },{
        'title': "Bachelor's",
        'value': 'bachelor',
    },{
        'title': "Master's",
        'value': 'master'
    }]
