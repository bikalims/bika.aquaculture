# -*- coding: utf-8 -*-

import six
from Products.Archetypes import public
from archetypes.schemaextender.interfaces import IExtensionField
from plone import api as ploneapi
from zope.interface import implements

from bika.aquaculture.config import _
from bika.lims import api
from senaite.core.catalog import SAMPLE_CATALOG


class SamplerExtensionField(object):
    """Mix-in class to make Archetypes fields not depend on generated
    accessors and mutators, and use AnnotationStorage by default.
    """

    implements(IExtensionField)
    storage = public.AnnotationStorage()

    def __init__(self, *args, **kwargs):
        super(SamplerExtensionField, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

    def getAccessor(self, instance):
        def accessor():
            return self.get(instance)

        return accessor

    def getEditAccessor(self, instance):
        def edit_accessor():
            return self.getRaw(instance)

        return edit_accessor

    def getMutator(self, batch):
        def mutator(value, **kw):
            old_value = batch.getField("Sampler").get(batch)
            pu = api.get_tool("plone_utils")
            change_samples = False
            if old_value != value:
                query = {
                    "getBatchUID": batch.UID(),
                    "portal_type": "AnalysisRequest",
                    "getDateVerified": {"query": "", "range": "min"},
                }
                brains = api.search(query, SAMPLE_CATALOG)
                if brains:
                    message = _(
                        """Case sampler cannot  be modified - the case
                                   contains verified specimen"""
                    )
                    pu.addPortalMessage(message, "error")
                    change_samples = False
                else:
                    change_samples = True

            if change_samples:
                samples = batch.getAnalysisRequests()
                for sample in samples:
                    sample.Sampler = value
                    sample.reindexObject()
                if samples:
                    user = ploneapi.user.get(userid=value)
                    fullname = user.getProperty("fullname")
                    message = _(
                        """Changed the sampler on child specimen of this
                                   case to {}"""
                    ).format(fullname)
                    pu.addPortalMessage(message, "info")
                self.set(batch, value)

        return mutator

    def getIndexAccessor(self, instance):
        name = getattr(self, "index_method", None)
        if name is None or name == "_at_accessor":
            return self.getAccessor(instance)
        elif name == "_at_edit_accessor":
            return self.getEditAccessor(instance)
        elif not isinstance(name, six.string_types):
            raise ValueError("Bad index accessor value: %r", name)
        else:
            return getattr(instance, name)


class RoutineExtensionField(object):
    """Mix-in class to make Archetypes fields not depend on generated
    accessors and mutators, and use AnnotationStorage by default.
    """

    implements(IExtensionField)
    storage = public.AnnotationStorage()

    def __init__(self, *args, **kwargs):
        super(RoutineExtensionField, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs

    def getAccessor(self, instance):
        def accessor():
            return self.get(instance)

        return accessor

    def getEditAccessor(self, instance):
        def edit_accessor():
            return self.getRaw(instance)

        return edit_accessor

    def getMutator(self, batch):
        def mutator(value, **kw):
            old_value = batch.getField("BatchPriority").get(batch)
            pu = api.get_tool("plone_utils")
            change_samples = False
            if old_value != value:
                query = {
                    "getBatchUID": batch.UID(),
                    "portal_type": "AnalysisRequest",
                    "getDateVerified": {"query": "", "range": "min"},
                }
                brains = api.search(query, SAMPLE_CATALOG)
                if brains:
                    message = _(
                        """Case routine cannot  be modified - the case
                                   contains verified specimen"""
                    )
                    pu.addPortalMessage(message, "error")
                    change_samples = False
                else:
                    change_samples = True

            if change_samples:
                samples = batch.getAnalysisRequests()
                priority = "3"
                if value == "rush":
                    priority = "1"
                for sample in samples:
                    sample.Priority = priority
                    sample.reindexObject()
                if samples:
                    message = _(
                        """Changed the priority on child specimen of this
                                   case to {}"""
                    ).format(value)
                    pu.addPortalMessage(message, "info")
                self.set(batch, value)

        return mutator

    def getIndexAccessor(self, instance):
        name = getattr(self, "index_method", None)
        if name is None or name == "_at_accessor":
            return self.getAccessor(instance)
        elif name == "_at_edit_accessor":
            return self.getEditAccessor(instance)
        elif not isinstance(name, six.string_types):
            raise ValueError("Bad index accessor value: %r", name)
        else:
            return getattr(instance, name)


class ExtSamplerStringField(SamplerExtensionField, public.StringField):
    "Field extender"


class ExtRoutineExtensionField(RoutineExtensionField, public.StringField):
    "Field extender"
