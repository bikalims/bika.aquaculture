# -*- coding: utf-8 -*-
from bika.aquaculture.behaviors.ext_sample_point import IExtSamplePointMarker
from bika.aquaculture.testing import BIKA_AQUACULTURE_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class ExtSamplePointIntegrationTest(unittest.TestCase):

    layer = BIKA_AQUACULTURE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_ext_sample_point(self):
        behavior = getUtility(IBehavior, 'bika.aquaculture.ext_sample_point')
        self.assertEqual(
            behavior.marker,
            IExtSamplePointMarker,
        )
