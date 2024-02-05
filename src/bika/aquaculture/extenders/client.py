# -*- coding: utf-8 -*-

import plone
from Products.Archetypes.Widget import BooleanWidget
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.component import adapts
from zope.interface import implementer
from bika.lims.browser.widgets import ARTemplatePartitionsWidget as ARTPW
import json
from operator import itemgetter

from bika.aquaculture.config import _
from bika.aquaculture.interfaces import IBikaAquacultureLayer
from bika.extras.extenders.fields import ExtBooleanField
from bika.extras.extenders.fields import ExtRecordsField
from bika.lims import api
from bika.lims.interfaces import IClient
from senaite.core.catalog import SETUP_CATALOG
from Products.Archetypes.Registry import registerWidget


class ClientSuppliersWidget(ARTPW):
    """
    """


registerWidget(ClientSuppliersWidget,
               title='Client Supplier Widget',
               description=('AR Template Partition Layout'),
               )

postal_mail_field = ExtBooleanField(
    "PostalMail",
    mode="rw",
    schemata="Preferences",
    widget=BooleanWidget(
        label=_("Postal Mail"),
        format='select',
    )
)

couriers_field = ExtRecordsField(
    "Couriers",
    schemata="Preferences",
    required=0,
    type="Courier",
    subfields=(
        "Supplier",
        "AccountNumber",
    ),
    subfield_labels={
        "Supplier": _("Supplier"),
        "AccountNumber": _("Account number"),
        "supplier_uid": "",
    },
    subfield_sizes={
        "Supplier": 35,
    },
    subfield_hidden={
        "supplier_uid": True,
    },
    default=[{
        "Supplier": "",
        "supplier_uid": "",
        "AccountNumber": "",
    }],
    widget=ClientSuppliersWidget(
        label=_("Couriers"),
        combogrid_options={
            "Supplier": {
                "colModel": [
                    {
                        "columnName": "supplier_uid",
                        "hidden": True},
                    {
                        "columnName": "Supplier",
                        "width": "30",
                        "label": _("Supplier")
                    }],
                "url": "getsuppliers",
                "showOn": True,
                "width": "550px"
            },
        },
    ),
)


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class ClientSchemaExtender(object):
    adapts(IClient)
    layer = IBikaAquacultureLayer

    fields = [
        postal_mail_field,
        couriers_field,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields


class ajaxGetSuppliers:

    catalog_name = 'senaite_catalog_setup'
    contentFilter = {'portal_type': 'Supplier',
                     'is_active': True}

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        plone.protect.CheckAuthenticator(self.request)
        searchTerm = 'searchTerm' in self.request and self.request[
            'searchTerm'].lower() or ''
        page = self.request['page']
        nr_rows = self.request['rows']
        sord = self.request['sord']
        sidx = self.request['sidx']
        rows = []

        # lookup objects from ZODB
        catalog = api.get_tool(SETUP_CATALOG)
        brains = catalog(self.contentFilter)
        brains = searchTerm and \
            [p for p in brains if p.Title.lower().find(searchTerm) > -1] \
            or brains

        rows = [{'UID': p.UID,
                 'supplier_uid': p.UID,
                 'Supplier': p.Title,
                 'AccountNumber': p.getObject().getAccountNumber()}
                for p in brains]

        rows = sorted(rows, cmp=lambda x, y: cmp(x.lower(
        ), y.lower()), key=itemgetter(sidx and sidx or 'Supplier'))
        if sord == 'desc':
            rows.reverse()
        pages = len(rows) / int(nr_rows)
        pages += divmod(len(rows), int(nr_rows))[1] and 1 or 0
        ret = {'page': page,
               'total': pages,
               'records': len(rows),
               'rows': rows[(int(page) - 1) * int(nr_rows): int(page) * int(nr_rows)]}
        return json.dumps(ret)
