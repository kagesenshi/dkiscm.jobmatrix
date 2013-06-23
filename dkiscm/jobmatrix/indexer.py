from plone.indexer import indexer
from dkiscm.jobmatrix.content.job import IJob
from dkiscm.jobmatrix.content.industrycluster import IIndustryCluster
from dkiscm.jobmatrix.content.jobgroup import IJobGroup
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

@indexer(IJob)
def job_industry_cluster(obj):
    if IIndustryCluster.providedBy(obj.__parent__):
        return obj.__parent__.id
    if IJobGroup.providedBy(obj.__parent__):
        jobgroup = obj.__parent__
        if IIndustryCluster.providedBy(jobgroup.__parent__):
            return jobgroup.__parent__.id
    return 'no-industry-cluster'

@indexer(IJob)
def job_exp_levels(obj):
    if obj.exp_levels:
        return obj.exp_levels

    vocab = getUtility(IVocabularyFactory,
            name='dkiscm.jobmatrix.experience')(obj)
    keys = [i.value for i in vocab]
    cols = {}
    for s in (obj.skills_competency or []):
        for col in s:
            if col not in keys:
                continue
            cols.setdefault(col, [])
            if s[col]:
                cols[col].append(s[col])
    exp_levels = [c for c in cols if cols[c]]
    obj.exp_levels = exp_levels
    return exp_levels
