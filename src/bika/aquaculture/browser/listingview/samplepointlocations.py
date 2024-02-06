# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from bika.aquaculture.config import _
from bika.aquaculture.config import is_installed
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter


class SamplePointLocationsListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        if not is_installed():
            return
        self.listing.title = self.context.translate("Pond Locations")
        spl = "sample_point_location_id"
        if spl in self.listing.columns:
            self.listing.columns[spl]["title"] = _("Pond Location ID")

    def folder_item(self, obj, item, index):
        if not is_installed():
            return item
        return item
