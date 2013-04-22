from collective.grok import gs
from Products.CMFCore.utils import getToolByName

# -*- extra stuff goes here -*- 


@gs.upgradestep(title=u'Upgrade dkiscm.jobmatrix to 1002',
                description=u'Upgrade dkiscm.jobmatrix to 1002',
                source='1001', destination='1002',
                sortkey=1, profile='dkiscm.jobmatrix:default')
def to1002(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-dkiscm.jobmatrix.upgrades:to1002')


@gs.upgradestep(title=u'Upgrade dkiscm.jobmatrix to 1001',
                description=u'Upgrade dkiscm.jobmatrix to 1001',
                source='1000', destination='1001',
                sortkey=1, profile='dkiscm.jobmatrix:default')
def to1001(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-dkiscm.jobmatrix.upgrades:to1001')
