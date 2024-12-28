# -*- coding: utf-8 -*-

from Products.Archetypes.Widget import RichWidget
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.component import adapts
from zope.interface import implementer

from bika.aquaculture.config import _
from bika.aquaculture.interfaces import IBikaAquacultureLayer
from bika.extras.extenders.fields import ExtTextField
from bika.lims.interfaces import ILaboratory

coa_disclamer_field = ExtTextField(
    'COADisclamer',
    default_content_type='text/html',
    default_output_type='text/x-html-safe',
    widget=RichWidget(
        label=_('COA Disclamer'),
        allow_file_upload=False,
        default_mime_type='text/x-rst',
        output_mime_type='text/x-html',
    ),
)


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class LaboratorySchemaExtender(object):
    adapts(ILaboratory)
    layer = IBikaAquacultureLayer

    fields = [
        coa_disclamer_field,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields
