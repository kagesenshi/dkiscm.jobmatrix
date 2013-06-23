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
        vocab = getUtility(
            IVocabularyFactory,
            name='dkiscm.jobmatrix.experienceyears'
        )(self.context)

        result = []
        levels = [i.value for i in self.exp_levels()]
        return [i for i in vocab if i.value in levels]

    def job_grouping(self):
        parent = aq_parent(self.context)
        if not IJobGroup.providedBy(parent):
            return []

        parent_container = aq_parent(parent)
        groups = []
        for o in parent_container.values():
            if IJobGroup.providedBy(o):
                data = {
                    'title': o.pretty_title_or_id(),
                    'css_class': ''
                }
                if o == parent:
                    data['css_class'] = 'selected-group'
                groups.append(data)
        return groups

    def education(self):
        selected = self.context.education
        vocab = getUtility(IVocabularyFactory,
                name='dkiscm.jobmatrix.education')(self.context)
        result = []
        for term in vocab:
            data = {
                'title': term.title,
                'css_class': ''
            }

            if term.value == selected:
                data['css_class'] = 'selected-education'

            result.append(data)

        return result

    def exp_levels(self):
        vocab = getUtility(IVocabularyFactory,
            name='dkiscm.jobmatrix.experience')(self.context)
        result = []
        for exp in self.context.exp_levels:
            result.append(vocab.getTerm(exp))
        return result

    def softskills_competency_columns(self):
        competencies = self.context.softskills_competency
        cols = {}
        for c in competencies:
            for col in c:
                cols.setdefault(col, [])
                if c[col]:
                    cols[col].append(c[col])
        return sorted([c for c in cols if cols[c]])

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
