# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import polklibrary.archives.ohms


class PolklibraryArchivesOhmsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=polklibrary.archives.ohms)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'polklibrary.archives.ohms:default')


POLKLIBRARY_ARCHIVES_OHMS_FIXTURE = PolklibraryArchivesOhmsLayer()


POLKLIBRARY_ARCHIVES_OHMS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(POLKLIBRARY_ARCHIVES_OHMS_FIXTURE,),
    name='PolklibraryArchivesOhmsLayer:IntegrationTesting'
)


POLKLIBRARY_ARCHIVES_OHMS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(POLKLIBRARY_ARCHIVES_OHMS_FIXTURE,),
    name='PolklibraryArchivesOhmsLayer:FunctionalTesting'
)


POLKLIBRARY_ARCHIVES_OHMS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        POLKLIBRARY_ARCHIVES_OHMS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='PolklibraryArchivesOhmsLayer:AcceptanceTesting'
)
