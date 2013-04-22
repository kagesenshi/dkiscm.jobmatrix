from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.app.content.interfaces import INameFromTitle
from dkiscm.jobmatrix import MessageFactory as _

class INameFromJobCode(INameFromTitle):
    """
       Marker/Form interface for NameFromJobCode
    """

class NameFromJobCode(object):
    """
       Adapter for NameFromJobCode
    """
    implements(INameFromJobCode)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context
    
    @property
    def title(self):
        return self.context.job_code
