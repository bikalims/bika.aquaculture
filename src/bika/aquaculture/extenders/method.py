# -*- coding: utf-8 -*-

from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.interfaces import IMethod
from bika.aquaculture.config import _
from bika.aquaculture.config import is_installed
from zope.component import adapts
from zope.interface import implements


class MethodSchemaModifier(object):
    adapts(IMethod)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """
        """
        if is_installed():
            schema["MethodID"].widget.label = _("Protocol")
            schema["MethodDocument"].widget.label = _("Protocol Document")

        return schema
