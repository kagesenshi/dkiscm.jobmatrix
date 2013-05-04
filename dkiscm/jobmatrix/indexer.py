from plone.indexer import indexer
from dkiscm.jobmatrix.content.job import IJob
from dkiscm.jobmatrix.content.industrycluster import IIndustryCluster
from dkiscm.jobmatrix.content.jobgroup import IJobGroup

@indexer(IJob)
def job_industry_cluster(obj):
    if IIndustryCluster.providedBy(obj.__parent__):
        return obj.__parent__.id
    if IJobGroup.providedBy(obj.__parent__):
        jobgroup = obj.__parent__
        if IIndustryCluster.providedBy(jobgroup.__parent__):
            return jobgroup.__parent__.id
    return 'no-industry-cluster'
