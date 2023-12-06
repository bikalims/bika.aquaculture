# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

from bika.aquaculture.config import _
from bika.aquaculture.config import PROFILE_ID
from bika.aquaculture.config import logger
from bika.lims import api
from senaite.core.setuphandlers import add_dexterity_items


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'bika.aquaculture:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    logger.info("BIKA.AQUACULTURE post install handler [BEGIN]")
    profile_id = PROFILE_ID
    context = context._getImportContext(profile_id)
    portal = context.getSite()
    setup(portal)
    add_dexterity_setup_items(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def add_dexterity_setup_items(portal):
    """Adds the Dexterity Container in the Setup Folder

    N.B.: We do this in code, because adding this as Generic Setup Profile in
          `profiles/default/structure` flushes the contents on every import.
    """
    # Tuples of ID, Title, FTI
    items = [
        ("purpose_of_testing_folder",
         "Purpose of Testing Folder",
         "PurposeOfTestingFolder"),
        ("payment_method_folder",
         "Payment Methods",
         "PaymentMethodFolder"),
        ("species_folder",
         "Species",
         "SpeciesFolder"),
    ]
    setup = api.get_setup()
    add_dexterity_items(setup, items)


def setup(portal):
    # Batches
    batches = portal['batches']
    batches.title = _('Cases')
    batches.reindexObject()

    # pt
    pt = api.get_tool("portal_types", context=portal)
    # Batch
    fti = pt.get("Batch")
    fti.title = _('Case')

    # Methods
    methods = portal['methods']
    methods.title = 'Protocols'
    methods.reindexObject()
    # Method
    fti = pt.get("Method")
    fti.title = _('Protocol')

    # Client
    fti = pt.get("Client")
    actions = fti.listActions()
    for idx, action in enumerate(actions):
        if action.title == "Batches":
            action.title = _("Cases")
        if action.title == "Sample Points":
            action.title = _("Ponds")

    # Sample Types
    portal['bika_setup']["bika_sampletypes"].setTitle("Specimen Types")
    # Sample Type
    fti = pt.get("SampleType")
    fti.title = _('Specimen Type')

    # Sample Points
    portal['bika_setup']["bika_samplepoints"].setTitle("Ponds")
    # Sample Type
    fti = pt.get("SamplePoint")
    fti.title = _('Pond')

    logger.info("BIKA.AQUACULTURE setup [DONE]")
