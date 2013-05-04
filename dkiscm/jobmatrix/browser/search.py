from five import grok
from Products.ATContentTypes.interfaces.topic import IATTopic
from plone.app.collection.interfaces import ICollection
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility

grok.templatedir('templates')

class BaseJobSearch(grok.View):
    grok.baseclass()
    grok.name('jobsearch')
    grok.require('zope2.View')
    grok.template('jobsearch')

    def industry_clusters(self):
        return getUtility(
            IVocabularyFactory,
            name='dkiscm.jobmatrix.industrycluster'
        )(self.context)

    def experience_years(self):
        return getUtility(
            IVocabularyFactory,
            name='dkiscm.jobmatrix.experienceyears'
        )(self.context)


class TopicJobSearch(BaseJobSearch):
    grok.context(IATTopic)

class CollectionJobSearch(BaseJobSearch):
    grok.context(ICollection)


class BaseJobSearchResults(grok.View):
    grok.baseclass()
    grok.name('jobsearch_results')
    grok.require('zope2.View')
    grok.template('jobsearch_results')

    def results(self):
        query = self.context.buildQuery()
        query.update(self.buildFilterQuery())
        catalog = self.context.portal_catalog

        results = []
        for brain in catalog(query):
            results.append(self._extract(brain))

        return results
    
    def buildFilterQuery(self):
        result = {}
        if self.request.get('industry_cluster', None):
            result['industry_cluster'] = self.request.get('industry_cluster')
        if self.request.get('job_title', None):
            result['Title'] = self.request.get('job_title')
        if self.request.get('searchtext', None):
            result['SearchableText'] = self.request.get('searchtext')
        return result

    def _extract(self, brain):
        return {
            'title': brain.Title,
            'url': brain.getURL() + '/level_view?lvl=' + self.request.get('experience', ''),
        }

class TopicJobSearchResults(BaseJobSearchResults):
    grok.context(IATTopic)

class CollectionJobSearchResults(BaseJobSearchResults):
    grok.context(ICollection)

