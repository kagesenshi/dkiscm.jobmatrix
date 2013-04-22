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
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from collective.z3cform.datagridfield.datagridfield import (
        DataGridField
)
import re

from z3c.form.interfaces import IFormLayer, IFieldWidget
import zope.schema.interfaces
import zope.component
import zope.interface
from z3c.form.widget import FieldWidget


class SingleDataGridField(DataGridField):

    allow_insert = False
    auto_append = False
    allow_delete = False

    def updateWidgets(self):
        super(SingleDataGridField, self).updateWidgets()
        template = self.getWidget('AA')
        template.klass = 'datagridwidget-row'
        self.widgets.append(template)

@zope.component.adapter(zope.schema.interfaces.IField, IFormLayer)
@zope.interface.implementer(IFieldWidget)
def SingleDataGridFieldFactory(field, request):
    """IFieldWidget factory for DataGridField."""
    return FieldWidget(field, SingleDataGridField(request))



# Interface class; used to define content-type schema.
class InvalidIntegerRange(schema.ValidationError):
    __doc__ = u'Please enter range using [start]-[end] format. eg: 3-6'

def isIntRange(value):
    if not value:
        return True
    if not re.match('(\d+)-(\d+)', value):
        raise InvalidIntegerRange()
    return True

EMPTY_ROW={
    'entry': '',
    'intermediate':'',
    'senior':'',
    'advanced':'',
    'master':''
}

class IIntRangeGrid(form.Schema):
    entry = schema.TextLine(
        title=_(u'Entry'),
        description=u'Please enter in format [start]-[end] (eg: 3-6)',
        required=False,
        constraint=isIntRange,
        default=u'',
    )

    intermediate = schema.TextLine(
        title=_(u'Intermediate'),
        description=u'Please enter in format [start]-[end] (eg: 3-6)',
        required=False,
        constraint=isIntRange,
        default=u'',
    )

    senior = schema.TextLine(
        title=_(u'Senior'),
        description=u'Please enter in format [start]-[end] (eg: 3-6)',
        required=False,
        constraint=isIntRange,
        default=u'',
    )

    advanced = schema.TextLine(
        title=_(u'Advanced'),
        description=u'Please enter in format [start]-[end] (eg: 3-6)',
        required=False,
        constraint=isIntRange,
        default=u'',
    )

    master = schema.TextLine(
        title=_(u'Master'),
        description=u'Please enter in format [start]-[end] (eg: 3-6)',
        required=False,
        constraint=isIntRange,
        default=u'',
    )


class IIndustryExperienceGrid(IIntRangeGrid):
    pass

class ISalaryRangeGrid(IIntRangeGrid):
    pass

class IIndustryCertificationGrid(form.Schema):

    entry = schema.Text(
        title=_(u'Entry'),
        required=False,
        default=u'',
    )

    intermediate = schema.Text(
        title=_(u'Intermediate'),
        required=False,
        default=u'',
    )

    senior = schema.Text(
        title=_(u'Senior'),
        required=False,
        default=u'',
    )

    advanced = schema.Text(
        title=_(u'Advanced'),
        required=False,
        default=u'',
    )

    master = schema.Text(
        title=_(u'Master'),
        required=False,
        default=u'',
    )

class ISkillGrid(form.Schema):

    skill = schema.Text(
        title=_(u'Skill'),
        required=True,
        default=u'',
    )

    entry = schema.Text(
        title=_(u'Entry'),
        required=False,
        default=u'',
    )

    intermediate = schema.Text(
        title=_(u'Intermediate'),
        required=False,
        default=u'',
    )

    senior = schema.Text(
        title=_(u'Senior'),
        required=False,
        default=u'',
    )

    advanced = schema.Text(
        title=_(u'Advanced'),
        required=False,
        default=u'',
    )

    master = schema.Text(
        title=_(u'Master'),
        required=False,
        default=u'',
    )

    is_required=schema.Bool(
        title=_(u'Mark row as required'),
        default=False,
        required=False
    )

class ISoftSkillGrid(form.Schema):

    skill = schema.Text(
        title=_(u'Skill'),
        required=True,
        default=u'',
    )

    col1 = schema.Text(
        title=_(u'1'),
        required=False,
        default=u'',
    )

    col2 = schema.Text(
        title=_(u'2'),
        required=False,
        default=u'',
    )

    col3 = schema.Text(
        title=_(u'3'),
        required=False,
        default=u'',
    )

    col4 = schema.Text(
        title=_(u'4'),
        required=False,
        default=u'',
    )

    col5 = schema.Text(
        title=_(u'5'),
        required=False,
        default=u'',
    )

    is_required=schema.Bool(
        title=_(u'Mark row as required'),
        default=False,
        required=False
    )


class IJob(form.Schema, IImageScaleTraversable):
    """
    Description of the Example Type
    """

    job_code = schema.TextLine(
        title=_(u'Job Code'),
        required=True
    )

    industry_cluster = schema.Choice(
        title=_(u'Industry Cluster'),
        vocabulary='dkiscm.jobmatrix.industrycluster',
        required=True
    )

    job_grouping = schema.Choice(
        title=_(u'Job Grouping'),
        vocabulary='dkiscm.jobmatrix.jobgrouping',
        required=True
    )

    education = schema.Choice(
        title=_(u'Education'),
        vocabulary='dkiscm.jobmatrix.education',
        required=True
    )

    similar_jobs = RelationList(
        title=_(u'Similar Job Titles'),
        required=False,
        value_type=RelationChoice(
            source=ObjPathSourceBinder(object_provides='dkiscm.jobmatrix.content.job.IJob')
        )
    )

    form.widget(industry_experience=DataGridFieldFactory)
    industry_experience = schema.List(
        title=u'Industry Experience',
        value_type=DictRow(schema=IIndustryExperienceGrid),
    )

    form.widget(industry_certification=DataGridFieldFactory)
    industry_certification = schema.List(
        title=u'Industry Certification',
        value_type=DictRow(schema=IIndustryCertificationGrid),
        required=False,
    )

    form.widget(salary_range=DataGridFieldFactory)
    salary_range = schema.List(
        title=u'Salary Range',
        value_type=DictRow(schema=ISalaryRangeGrid),
        required=False,
    )

    form.widget(skills_competency=DataGridFieldFactory)
    skills_competency = schema.List(
        title=_(u'Technical Skills Competency'),
        value_type=DictRow(schema=ISkillGrid),
    )

    form.widget(softskills_competency=DataGridFieldFactory)
    softskills_competency = schema.List(
        title=_(u'Soft Skills Competency'),
        value_type=DictRow(schema=ISoftSkillGrid),
    )
