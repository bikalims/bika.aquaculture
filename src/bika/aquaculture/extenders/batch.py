# -*- coding: utf-8 -*-

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.interface import implements
from zope.component import adapts
from zope.interface import implementer
from Products.Archetypes.Widget import StringWidget

from bika.aquaculture.config import _
from bika.aquaculture.config import is_installed
from bika.aquaculture.interfaces import IBikaAquacultureLayer
from bika.extras.extenders.fields import ExtStringField
from bika.lims.interfaces import IBatch


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


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class BatchSchemaExtender(object):
    adapts(IBatch)
    layer = IBikaAquacultureLayer

    fields = [
        nan_field,
        reference_number_field,
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
