from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from dkiscm.jobmatrix import MessageFactory as _


# Interface class; used to define content-type schema.


class IIndustryCluster(form.Schema, IImageScaleTraversable):
    """
    Industry cluster
    """

    infobox_bgcolor = schema.TextLine(
        title=u'Infobox background color',
        description=u'Hex value of the color',
        default=u'#7F858E'
    )

    th_bgcolor = schema.TextLine(
        title=u'Table heading background color',
        description=u'Hex value of the color',
        default=u'#717171'
    )

    td_bgcolor = schema.TextLine(
        title=u'Cell background color',
        description=u'Hex value of the color',
        default=u'#eeeeee'
    )

    highlighted_td_bgcolor = schema.TextLine(
        title=u'Highlighted cell background color',
        description=u'Hex value of the color',
        default=u'#a5a5a5'
    )

    weight1_bgcolor = schema.TextLine(
        title=u'Weight 1 background color',
        default=u"#EFEAEA"
    )


    weight2_bgcolor = schema.TextLine(
        title=u'Weight 2 background color',
        default=u'#D2D2D2',
    )

    weight3_bgcolor = schema.TextLine(
        title=u'Weight 3 background color',
        default=u'#BBBBBB'
    )

    weight4_bgcolor = schema.TextLine(
        title=u'Weight 4 background color',
        default=u'#A9A9A9',
    )

    weight5_bgcolor = schema.TextLine(
        title=u'Weight 5 background color',
        default=u'#9A9A9A'
    )
