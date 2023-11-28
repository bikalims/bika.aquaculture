from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.interfaces import IAnalysisRequest
from bika.aquaculture.config import _
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
            schema['Batch'].widget.label = _("Case")
            schema['Batch'].widget.description = _("Assign a sample to a case")
            schema['ClientSampleID'].widget.label = _("Pool ID")
            schema['SampleType'].widget.label = _("Specimen Type")
            schema['SamplePoint'].widget.label = _("Pond")
            schema['SubGroup'].widget.label = _("Case Sub Group")
            schema['SubGroup'].widget.description = _("The assigned case sub group of this request")

        return schema
