from plone.indexer import indexer
from dkiscm.jobmatrix.content.job import IJob
from dkiscm.jobmatrix.content.industrycluster import IIndustryCluster

@indexer(IJob)
def job_industry_cluster(obj):
    if IIndustryCluster.providedBy(obj.__parent__):
        return obj.__parent__.id
    return 'no-industry-cluster'
