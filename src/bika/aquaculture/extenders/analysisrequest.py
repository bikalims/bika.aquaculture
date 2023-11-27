from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.interfaces import IAnalysisRequest
from bika.aquaculture.config import is_installed
from zope.component import adapts
from zope.interface import implements


class AnalysisRequestSchemaModifier(object):
    adapts(IAnalysisRequest)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """
        """
        if is_installed():
            schema['Batch'].widget.label = "Case"
            schema['Batch'].widget.description = "Assign a sample to a case"
            schema['ClientSampleID'].widget.label = "Pool ID"
            schema['SubGroup'].widget.label = "Case Sub Group"
            schema['SubGroup'].widget.description = "The assigned case sub group of this request"

        return schema
