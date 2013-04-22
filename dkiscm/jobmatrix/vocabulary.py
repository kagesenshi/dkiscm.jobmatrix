from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource
from Products.CMFCore.utils import getToolByName
from dkiscm.jobmatrix import MessageFactory as _

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

    terms = [{
        'title':_(u'Creative Multimedia'),
        'value': 'creative-multimedia'
    }]


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
