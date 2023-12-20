# -*- coding: utf-8 -*-

from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.Widget import StringWidget
from Products.CMFCore.permissions import View
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.interface import implements
from zope.component import adapts
from zope.interface import implementer
import six
from archetypes.schemaextender.interfaces import IExtensionField
from Products.Archetypes import public

from bika.aquaculture.config import _
from bika.aquaculture.config import is_installed
from bika.aquaculture.vocabularies import BATCH_PRIORITY
from bika.aquaculture.vocabularies import getUsers
from bika.aquaculture.vocabularies import get_countries
from bika.aquaculture.interfaces import IBikaAquacultureLayer
from bika.extras.extenders.fields import ExtStringField
from bika.extras.extenders.fields import ExtUIDReferenceField
from bika.lims import api
from bika.lims import FieldEditContact
from bika.lims.interfaces import IBatch
from senaite.core.catalog import SETUP_CATALOG
from senaite.core.catalog import SAMPLE_CATALOG
from senaite.core.browser.widgets.referencewidget import ReferenceWidget


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
            old_value = batch.getField('Sampler').get(batch)
            pu = api.get_tool("plone_utils")
            change_samples = False
            if old_value != value:
                query = {"getBatchUID": batch.UID(),
                         "portal_type": "AnalysisRequest",
                         "getDateVerified": {'query': '', 'range': 'min'},
                         }
                brains = api.search(query, SAMPLE_CATALOG)
                if brains:
                    message = _("""Cannot change sampler field because one of
                                speciman has been verified""")
                    pu.addPortalMessage(message, 'error')
                    change_samples = False
                else:
                    change_samples = True

            if change_samples:
                samples = batch.getAnalysisRequests()
                for sample in samples:
                    sample.Sampler = value
                    sample.reindexObject()
                message = _("""Changed child samples of this batch""")
                pu.addPortalMessage(message, 'info')
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


nan_field = ExtStringField(
    "NAN",
    mode="rw",
    schemata="default",
    widget=StringWidget(
        label=_(u"NAN"),
    ),
)

reference_number_field = ExtStringField(
    "ReferenceNumber",
    mode="rw",
    schemata="default",
    widget=StringWidget(
        label=_(u"Reference Number"),
    ),
)

purpose_of_testing_field = ExtUIDReferenceField(
    "PurposeOfTesting",
    required=False,
    allowed_types=("PurposeOfTesting",),
    multiValued=1,
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

country_of_origin_field = ExtStringField(
    "CountryOfOrigin",
    mode="rw",
    schemata="default",
    vocabulary=get_countries(),
    widget=SelectionWidget(
        label=_("Country of Origin"),
        format='select',
    )
)


destination_country_field = ExtStringField(
    "DestinationCountry",
    mode="rw",
    schemata="default",
    vocabulary=get_countries(),
    widget=SelectionWidget(
        label=_("Destination Country"),
        format='select',
    )
)

pooling_info_field = ExtStringField(
    "PoolingInfo",
    mode="rw",
    schemata="default",
    widget=StringWidget(
        label=_(u"Pooling Info"),
    ),
)

payment_method_field = ExtUIDReferenceField(
    "PaymentMethod",
    required=False,
    allowed_types=("PaymentMethod",),
    relationship="BatchPaymentMethod",
    format="select",
    mode="rw",
    read_permission=View,
    write_permission=FieldEditContact,
    widget=ReferenceWidget(
        label=_(u"Payment Method"),
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

batch_priority_field = ExtStringField(
    "BatchPriority",
    mode="rw",
    schemata="default",
    vocabulary=BATCH_PRIORITY,
    widget=SelectionWidget(
        label=_("Batch Priority"),
        description=_("Select batch priority"),
        format='select',
    )
)

sampler_field = ExtSamplerStringField(
    "Sampler",
    required=False,
    mode="rw",
    write_permission=FieldEditContact,
    vocabulary=getUsers(None, ["Sampler"]),
    widget=SelectionWidget(
        label=_("Sampler"),
        format='select',
    )
)


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class BatchSchemaExtender(object):
    adapts(IBatch)
    layer = IBikaAquacultureLayer

    fields = [
        nan_field,
        reference_number_field,
        purpose_of_testing_field,
        country_of_origin_field,
        pooling_info_field,
        destination_country_field,
        sampler_field,
        payment_method_field,
        batch_priority_field,
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
            schema['Sampler'].vocabulary = getUsers(self.context, ["Sampler"])
            schema['ClientBatchID'].widget.label = "Case Number"
            schema['BatchLabels'].widget.label = "Case Labels"
            schema['title'].widget.description = "If no Title value is entered, the Case ID will be used."

        return schema
