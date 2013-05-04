from five import grok
from Products.ATContentTypes.interfaces.topic import IATTopic
from plone.app.collection.interfaces import ICollection
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from dkiscm.jobmatrix.interfaces import IProductSpecific

grok.templatedir('templates')

class BaseJobSearch(grok.View):
    grok.baseclass()
    grok.name('jobsearch')
    grok.require('zope2.View')
    grok.template('jobsearch')
    grok.layer(IProductSpecific)

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
    grok.layer(IProductSpecific)

    def results(self):
        query = self.context.buildQuery()
        query.update(self.buildFilterQuery())
        catalog = self.context.portal_catalog

        results = []
        for brain in catalog(query):
            results.append(self._extract(brain))

        # redirect if theres only 1 result 
        if len(results) == 1:
            self.request.response.redirect(results[0]['url'])

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


class BaseJobSearchAutocomplete(grok.View):
    grok.baseclass()
    grok.name('jobtitle_autocomplete')
    grok.layer(IProductSpecific)

    def render(self):
        cluster = self.request.get('industry_cluster', '')
        query = self.request.get('q', '')
        results = []

        for job in self.context.portal_catalog(industry_cluster=cluster,
                portal_type='dkiscm.jobmatrix.job'):
            if job.Title.lower().startswith(query):
                results.append('|'.join((job.Title,job.Title)))
        return '\n'.join(results)

class TopicJobSearchAutocomplete(BaseJobSearchAutocomplete):
    grok.context(IATTopic)

class CollectionJobSearchAutocomplete(BaseJobSearchAutocomplete):
    grok.context(ICollection)
