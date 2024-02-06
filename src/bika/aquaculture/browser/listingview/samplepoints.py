# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from bika.aquaculture.config import _
from bika.aquaculture.config import is_installed
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter


class SamplePointsListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        if not is_installed():
            return
        self.listing.title = self.context.translate(_("Ponds"))
        if "Title" in self.listing.columns:
            self.listing.columns["Title"]["title"] = "Pond"
        if "SampleTypes" in self.listing.columns:
            self.listing.columns["SampleTypes"]["title"] = "Specimen Types"

    def folder_item(self, obj, item, index):
        if not is_installed():
            return item
        return item
