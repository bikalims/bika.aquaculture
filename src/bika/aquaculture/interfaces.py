# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from bika.lims.interfaces import IBikaLIMS
from senaite.samplepointlocations.interfaces import (
    ISenaiteSamplePointLocationsLayer,
)


class IBikaAquacultureLayer(IBikaLIMS, ISenaiteSamplePointLocationsLayer):
    """Zope 3 browser Layer interface specific for senaite.sampleimporter
    This interface is referred in profiles/default/browserlayer.xml.
    All views and viewlets register against this layer will appear in the site
    only when the add-on installer has been run.
    """


class IBikaSamplePointLocationsLayer(ISenaiteSamplePointLocationsLayer):
    """Zope 3 browser Layer interface specific for senaite.sampleimporter
    This interface is referred in profiles/default/browserlayer.xml.
    All views and viewlets register against this layer will appear in the site
    only when the add-on installer has been run.
    """


class IBikaBrowserAquacultureLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IPurposeOfTesting(Interface):
    """Marker interface for purposeoftesting
    """


class IPurposeOfTestingFolder(Interface):
    """Marker interface for purposeoftesting setup folder
    """


class IPaymentMethod(Interface):
    """Marker interface for payment method
    """


class IPaymentMethodFolder(Interface):
    """Marker interface for payment methods setup folder
    """


class ISpecies(Interface):
    """Marker interface for species
    """


class ISpeciesFolder(Interface):
    """Marker interface for species setup folder
    """


class ILifeStage(Interface):
    """Marker interface for Lifestage
    """


class ILifeStageFolder(Interface):
    """Marker interface for life stage setup folder
    """
