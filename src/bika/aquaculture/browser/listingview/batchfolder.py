# -*- coding: utf-8 -*-

from collections import OrderedDict
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
        keys = self.listing.columns.keys()
        keys.pop(-1)
        keys.insert(0, "Priority")
        new_cols = OrderedDict()
        for k in keys:
            new_cols[k] = self.listing.columns[k]
        self.listing.columns = new_cols

        for i in range(len(self.listing.review_states)):
            self.listing.review_states[i]["columns"].insert(0, "Priority")

        batch_id = "BatchID"
        if batch_id in self.listing.columns:
            self.listing.columns[batch_id]["title"] = _("Case ID")
        batch_labels = "BatchLabels"
        if batch_labels in self.listing.columns:
            self.listing.columns[batch_labels]["title"] = _("Case Labels")
        client_batch_id = "ClientBatchID"
        if client_batch_id in self.listing.columns:
            self.listing.columns[client_batch_id]["title"] = _("Client Case ID")

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
