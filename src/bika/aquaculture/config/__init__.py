# -*- coding: utf-8 -*-

import logging
from zope.i18nmessageid import MessageFactory

from bika.aquaculture.interfaces import IBikaAquacultureLayer
from bika.lims.api import get_request

PROFILE_ID = "profile-bika.aquaculture:default"
PROJECTNAME = "bika.aquaculture"

logger = logging.getLogger(PROJECTNAME)
_ = MessageFactory(PROJECTNAME)


def is_installed():
    """Returns whether the product is installed or not"""
    request = get_request()
    return IBikaAquacultureLayer.providedBy(request)
