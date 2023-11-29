from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.interfaces import IBatch
from bika.aquaculture.config import is_installed
from zope.component import adapts
from zope.interface import implements


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
