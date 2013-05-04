from five import grok
from plone.directives import dexterity, form
from dkiscm.jobmatrix.content.job import IJob
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from Acquisition import aq_parent
from dkiscm.jobmatrix.content.jobgroup import IJobGroup

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IJob)
    grok.require('zope2.View')
    grok.template('job_view')
    grok.name('view')

    def industry_experience(self):
        return getUtility(
            IVocabularyFactory,
            name='dkiscm.jobmatrix.experienceyears'
        )(self.context)

    def job_grouping(self):
        parent = aq_parent(self.context)
        if not IJobGroup.providedBy(parent):
            return ''
        return parent.pretty_title_or_id()

class LevelView(dexterity.DisplayForm):
    grok.context(IJob)
    grok.require('zope2.View')
    grok.template('level_view')
    grok.name('level_view')

    def leveldata(self):
        context = self.context
        lvl = self.request.get('lvl', None)
        vocab = getUtility(
            IVocabularyFactory,
            name='dkiscm.jobmatrix.experienceyears'
        )(context)

        result = {
            'industry_certification': '',
            'salary_range': '',
            'skills_competency': [],
        }

        if not lvl or lvl not in [i.value for i in vocab]:
            return result

        if context.industry_certification:
            industry_certification = context.industry_certification[0][lvl]
            result['industry_certification'] = industry_certification

        if context.salary_range:
            salary_range = context.salary_range[0][lvl]
            result['salary_range'] = salary_range

        if context.skills_competency:
            for val in context.skills_competency:
                result['skills_competency'].append({
                    'value': val[lvl],
                    'required': val['is_required']
                })

        return result
