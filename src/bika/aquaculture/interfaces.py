# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBikaAquacultureLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPurposeOfTestingFolder(Interface):
    """Marker interface for purposeoftesting setup folder
    """


class IPaymentMethodFolder(Interface):
    """Marker interface for payment methods setup folder
    """

class ISpeciesFolder(Interface):
    """Marker interface for species setup folder
    """
