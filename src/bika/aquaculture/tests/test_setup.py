# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from bika.aquaculture.testing import BIKA_AQUACULTURE_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that bika.aquaculture is properly installed."""

    layer = BIKA_AQUACULTURE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if bika.aquaculture is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'bika.aquaculture'))

    def test_browserlayer(self):
        """Test that IBikaAquacultureLayer is registered."""
        from bika.aquaculture.interfaces import (
            IBikaAquacultureLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IBikaAquacultureLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = BIKA_AQUACULTURE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['bika.aquaculture'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if bika.aquaculture is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'bika.aquaculture'))

    def test_browserlayer_removed(self):
        """Test that IBikaAquacultureLayer is removed."""
        from bika.aquaculture.interfaces import \
            IBikaAquacultureLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IBikaAquacultureLayer,
            utils.registered_layers())
