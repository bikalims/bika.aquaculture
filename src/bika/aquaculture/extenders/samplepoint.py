from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.interfaces import ISamplePoint
from bika.aquaculture.config import _
from bika.aquaculture.config import is_installed
from bika.aquaculture.interfaces import IBikaAquacultureLayer
from zope.component import adapts
from zope.interface import implements


class SamplePointSchemaModifier(object):
    adapts(ISamplePoint)
    implements(ISchemaModifier)
    layer = IBikaAquacultureLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """
        """
        if is_installed():
            schema["SampleTypes"].widget.label = _("Specimen Types")
            schema["SampleTypes"].widget.description = _(
                """The list of sample types that can be collected at this
                       sample point. If no sample types are selected, then all
                       sample types are available."""
            )
            schema["SamplePointId"].widget.label = "Pond ID"
            schema["SamplePointLocation"].widget.label = "Pond Location"

        return schema
