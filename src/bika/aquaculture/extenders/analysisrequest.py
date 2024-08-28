# -*- coding: utf-8 -*-

from Products.Archetypes.Widget import IntegerWidget
from Products.Archetypes.Widget import StringWidget
from Products.CMFCore.permissions import View
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from zope.interface import implements
from zope.component import adapts
from zope.interface import implementer

from bika.aquaculture.config import _
from bika.aquaculture.config import is_installed
from bika.aquaculture.interfaces import IBikaAquacultureLayer
from bika.aquaculture.vocabularies import SEXES
from bika.extras.extenders.fields import ExtStringField, ExtIntegerField
from bika.extras.extenders.fields import ExtUIDReferenceField
from bika.lims import FieldEditContact
from bika.lims import SETUP_CATALOG
from bika.lims.interfaces import IAnalysisRequest
from bika.lims.interfaces import IBatch
from bika.lims.browser.widgets import SelectionWidget
from senaite.core.browser.widgets.referencewidget import ReferenceWidget


pool_id_field = ExtStringField(
    "PoolID",
    required=False,
    mode="rw",
    read_permission=View,
    write_permission=FieldEditContact,
    widget=StringWidget(
        label=_(u"Pool ID"),
        description=_("Pool ID"),
        render_own_label=True,
        visible={
            "add": "edit",
            "header_table": "visible",
            "secondary": "disabled",
            "verified": "view",
            "published": "view",
        },
    ),
)
lot_field = ExtStringField(
    "Lot",
    required=False,
    mode="rw",
    read_permission=View,
    write_permission=FieldEditContact,
    widget=StringWidget(
        label=_(u"Lot"),
        description=_("Lot"),
        render_own_label=True,
        visible={
            "add": "edit",
            "header_table": "visible",
            "secondary": "disabled",
            "verified": "view",
            "published": "view",
        },
    ),
)

species_field = ExtUIDReferenceField(
    "Species",
    required=False,
    allowed_types=("Species",),
    relationship="AnalysisRequestSpecies",
    format="select",
    mode="rw",
    read_permission=View,
    write_permission=FieldEditContact,
    widget=ReferenceWidget(
        label=_(u"Species"),
        description=_("Select the species"),
        render_own_label=True,
        size=20,
        catalog_name=SETUP_CATALOG,
        base_query={"sort_on": "sortable_title", "is_active": True},
        showOn=True,
        visible={
            "add": "edit",
            "header_table": "visible",
            "secondary": "disabled",
            "verified": "view",
            "published": "view",
        },
        ui_item="title",
        colModel=[
            dict(columnName="UID", hidden=True),
            dict(columnName="title", width="60", label=_("Title")),
        ],
    ),
)

life_stage_field = ExtUIDReferenceField(
    "LifeStage",
    required=False,
    allowed_types=("LifeStage",),
    relationship="AnalysisRequestLifeStage",
    format="select",
    mode="rw",
    read_permission=View,
    write_permission=FieldEditContact,
    widget=ReferenceWidget(
        label=_(u"Life Stage"),
        description=_("Life stage"),
        render_own_label=True,
        size=20,
        catalog_name=SETUP_CATALOG,
        base_query={"sort_on": "sortable_title", "is_active": True},
        showOn=True,
        visible={
            "add": "edit",
            "header_table": "visible",
            "secondary": "disabled",
            "verified": "view",
            "published": "view",
        },
        ui_item="title",
        colModel=[
            dict(columnName="UID", hidden=True),
            dict(columnName="title", width="60", label=_("Title")),
        ],
    ),
)

number_of_animals_field = ExtIntegerField(
    "NumberOfAnimals",
    mode="rw",
    widget=IntegerWidget(
        label=_(u"Number Of Animals"),
        description=_("Number of animals."),
        render_own_label=True,
        visible={
            "add": "edit",
            "header_table": "visible",
            "secondary": "disabled",
            "verified": "view",
            "published": "view",
        },
    ),
)

sex_field = ExtStringField(
    "Sex",
    mode="rw",
    vocabulary=SEXES,
    widget=SelectionWidget(
        label=_("Sex"),
        description=_("Select sex of the sample."),
        render_own_label=True,
        showOn=True,
        format="select",
        visible={
            "add": "edit",
            "header_table": "visible",
            "secondary": "disabled",
            "verified": "view",
            "published": "view",
        },
    ),
)


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    layer = IBikaAquacultureLayer

    fields = [
        pool_id_field,
        lot_field,
        species_field,
        life_stage_field,
        number_of_animals_field,
        sex_field,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields


class AnalysisRequestSchemaModifier(object):
    adapts(IAnalysisRequest)
    implements(ISchemaModifier)
    layer = IBikaAquacultureLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """
        """
        if is_installed():
            schema["Batch"].widget.label = _("Case")
            schema["Batch"].widget.description = _("Assign a sample to a case")
            schema["SampleType"].widget.label = _("Specimen Type")
            schema["SampleType"].widget.description = _(
                "Select the specimen type of this specimen"
            )
            schema["SamplePoint"].widget.label = _("Pond")
            schema["SamplePointLocation"].widget.label = "Pond Location"
            schema["SubGroup"].widget.label = _("Case Sub Group")
            schema["SubGroup"].widget.description = _(
                "The assigned case sub group of this request"
            )
            if schema.get("Sampler"):
                if IBatch.providedBy(self.context.aq_parent):
                    schema["Sampler"].default = self.context.aq_parent.Sampler

        return schema
