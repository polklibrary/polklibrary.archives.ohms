# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from polklibrary.archives.ohms.testing import POLKLIBRARY_ARCHIVES_OHMS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that polklibrary.archives.ohms is properly installed."""

    layer = POLKLIBRARY_ARCHIVES_OHMS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if polklibrary.archives.ohms is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('polklibrary.archives.ohms'))

    def test_browserlayer(self):
        """Test that IPolklibraryArchivesOhmsLayer is registered."""
        from polklibrary.archives.ohms.interfaces import IPolklibraryArchivesOhmsLayer
        from plone.browserlayer import utils
        self.assertIn(IPolklibraryArchivesOhmsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = POLKLIBRARY_ARCHIVES_OHMS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['polklibrary.archives.ohms'])

    def test_product_uninstalled(self):
        """Test if polklibrary.archives.ohms is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('polklibrary.archives.ohms'))

    def test_browserlayer_removed(self):
        """Test that IPolklibraryArchivesOhmsLayer is removed."""
        from polklibrary.archives.ohms.interfaces import IPolklibraryArchivesOhmsLayer
        from plone.browserlayer import utils
        self.assertNotIn(IPolklibraryArchivesOhmsLayer, utils.registered_layers())
