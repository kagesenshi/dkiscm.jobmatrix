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

    mapping = {
        'creative-multimedia': [{
            'title': 'Pre-Production',
            'value': 'preproduction'
        },{
            'title': 'Production',
            'value': 'production',
        },{
            'title': 'Post-Production',
            'value': 'postproduction'
        }],
        'system-design-development': [{
            'title': 'Architectural Design',
            'value': 'architectural-design',
        },{
            'title': 'IC Design',
            'value': 'ic-design',
        },{
            'title': 'System Design',
            'value': 'system-design',
        },{
            'title': 'Software Engineering',
            'value': 'software-engineering'
        }],
        'information-technology': [{
            'title': 'Software Development',
            'value': 'software-development',
        },{
            'title': 'Database Management',
            'value': 'database-management',
        },{
            'title': 'Technical Support',
            'value': 'technical-support',
        },{
            'title': 'IT Consulting',
            'value': 'it-consulting',
        },{
            'title': 'IT Sales & Marketing',
            'value': 'it-sales-marketing',
        },{
            'title': 'IT Management',
            'value': 'it-management',
        }],
        'shared-services-outsourcing': [{
            'title': 'Contact Centre',
            'value': 'contact-centre',
        },{
            'title': 'Finance & Accounting',
            'value': 'finance-accounting',
        },{
            'title': 'Human Resources',
            'value': 'human-resources'
        }]
    }

    def __call__(self, context):
        parent_id = None

        if IIndustryCluster.providedBy(context):
            parent_id = context.id

        if IIndustryCluster.providedBy(context.__parent__):
            parent_id = context.__parent__.id

        results = self.mapping.get(parent_id, [])
        terms = []
        for item in results:
            terms.append(SimpleTerm(**item))
        return SimpleVocabulary(terms)



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
