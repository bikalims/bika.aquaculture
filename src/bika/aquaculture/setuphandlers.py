# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

from bika.lims import api
from bika.aquaculture.config import PROFILE_ID
from bika.aquaculture.config import logger


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


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def setup(portal):
    pt = api.get_tool("portal_types", context=portal)
    # Batches
    batches = portal['batches']
    batches.title = 'Cases'
    batches.reindexObject()
    # Batch
    fti = pt.get("Batch")
    fti.title = 'Case'

    # Client
    fti = pt.get("Client")
    actions = fti.listActions()
    for idx, action in enumerate(actions):
        if action.title == "Batches":
            action.title = "Cases"

    logger.info("BIKA.AQUACULTURE setup [DONE]")
