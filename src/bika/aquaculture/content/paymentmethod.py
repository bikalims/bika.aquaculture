# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from bika.aquaculture.interfaces import IPaymentMethod
from bika.lims.interfaces import IDeactivable
from plone.dexterity.content import Container
from plone.supermodel import model
from senaite.core.catalog import SETUP_CATALOG
from bika.lims import api
from zope.interface import implementer


class IPaymentMethodSchema(model.Schema):
    """Marker interface and Dexterity Python Schema for PaymentMethod"""


@implementer(IPaymentMethod, IPaymentMethodSchema, IDeactivable)
class PaymentMethod(Container):
    """Content-type class for IPaymentMethod"""

    _catalogs = [SETUP_CATALOG]

    security = ClassSecurityInfo()

    @security.private
    def accessor(self, fieldname):
        """Return the field accessor for the fieldname"""
        schema = api.get_schema(self)
        if fieldname not in schema:
            return None
        return schema[fieldname].get

    @security.private
    def mutator(self, fieldname):
        """Return the field mutator for the fieldname"""
        schema = api.get_schema(self)
        if fieldname not in schema:
            return None
        result = schema[fieldname].set
        self.reindexObject()
        return result
