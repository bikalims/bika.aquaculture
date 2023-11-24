# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import bika.aquaculture


class BikaAquacultureLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=bika.aquaculture)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'bika.aquaculture:default')


BIKA_AQUACULTURE_FIXTURE = BikaAquacultureLayer()


BIKA_AQUACULTURE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(BIKA_AQUACULTURE_FIXTURE,),
    name='BikaAquacultureLayer:IntegrationTesting',
)


BIKA_AQUACULTURE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(BIKA_AQUACULTURE_FIXTURE,),
    name='BikaAquacultureLayer:FunctionalTesting',
)


BIKA_AQUACULTURE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        BIKA_AQUACULTURE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='BikaAquacultureLayer:AcceptanceTesting',
)
