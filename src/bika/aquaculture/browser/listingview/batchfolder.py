# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from bika.aquaculture.config import _
from bika.aquaculture.config import is_installed
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter


class BatchFolderContentsListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        if not is_installed():
            return
        self.listing.title = self.context.translate(_("Cases"))
        batch_priority = [
            ("Priority", {"toggle": False, "sortable": True, "title": ""},)
        ]
        self.listing.columns.update(batch_priority)
        for i in range(len(self.listing.review_states)):
            self.listing.review_states[i]["columns"].insert(0, "Priority")

    def folder_item(self, obj, item, index):
        if not is_installed():
            return item
        batch = obj.getObject()
        batch_priority = batch.BatchPriority
        priority = "3"
        priority_text = "Routine"
        if batch_priority == "rush":
            priority = "1"
            priority_text = "Rush"
        priority_div = """<div class="priority-ico priority-%s">
                          <span class="notext">%s</span><div>
                       """
        item["replace"]["Priority"] = priority_div % (priority, priority_text)

        return item
