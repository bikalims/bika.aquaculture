# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from bika.aquaculture.config import is_installed
from bika.aquaculture.config import _
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter


class SamplesListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        if not is_installed():
            return
        spt = "getSamplePointTitle"
        if spt in self.listing.columns:
            self.listing.columns[spt]["title"] = _("Pond")

        spl = "SamplePointLocation"
        if spl in self.listing.columns:
            self.listing.columns[spl]["title"] = _("Pond Location")

        stt = "getSampleTypeTitle"
        if stt in self.listing.columns:
            self.listing.columns[stt]["title"] = _("Specimen Type")

        loc = "location"
        if loc in self.listing.columns:
            self.listing.columns[loc]["title"] = _("Pond Location")

    def folder_item(self, obj, item, index):
        if not is_installed():
            return item
        return item
