# -*- coding: utf-8 -*-

from Products.Archetypes.Widget import StringWidget
from Products.CMFCore.permissions import View
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.interface import implements
from zope.component import adapts
from zope.interface import implementer

from bika.aquaculture.config import _
from bika.aquaculture.config import is_installed
from bika.aquaculture.interfaces import IBikaAquacultureLayer
from bika.extras.extenders.fields import ExtStringField
from bika.extras.extenders.fields import ExtUIDReferenceField
from bika.lims import FieldEditContact
from bika.lims import SETUP_CATALOG
from bika.lims.interfaces import IBatch
from senaite.core.browser.widgets.referencewidget import ReferenceWidget


nan_field = ExtStringField(
    "NAN",
    mode="rw",
    schemata="default",
    widget=StringWidget(
        label=_(u"NAN"),
        description=_(u"NAN"),
    ),
)

reference_number_field = ExtStringField(
    "ReferenceNumber",
    mode="rw",
    schemata="default",
    widget=StringWidget(
        label=_(u"Reference Number"),
        description=_(u"Reference Number"),
    ),
)

purpose_of_testing_field = ExtUIDReferenceField(
    "PurposeOfTesting",
    required=False,
    allowed_types=("PurposeOfTesting",),
    relationship="AnalysisRequestPurposeOfTesting",
    format="select",
    mode="rw",
    read_permission=View,
    write_permission=FieldEditContact,
    widget=ReferenceWidget(
        label=_(u"Purpose Of Testing"),
        render_own_label=False,
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


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class BatchSchemaExtender(object):
    adapts(IBatch)
    layer = IBikaAquacultureLayer

    fields = [
        nan_field,
        reference_number_field,
        purpose_of_testing_field,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields


class BatchSchemaModifier(object):
    adapts(IBatch)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """
        """
        if is_installed():
            schema['ClientBatchID'].widget.label = "Case Number"
            schema['BatchLabels'].widget.label = "Case Labels"

        return schema
