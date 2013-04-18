from collective.grok import gs
from dkiscm.jobmatrix import MessageFactory as _

@gs.importstep(
    name=u'dkiscm.jobmatrix', 
    title=_('dkiscm.jobmatrix import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('dkiscm.jobmatrix.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
