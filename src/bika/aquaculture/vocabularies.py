# -*- coding: utf-8 -*-

from bika.aquaculture.config import _
from senaite.core.api import geo

BATCH_PRIORITY = [
    (_("Routine"), _("Routine")),
    (_("Rush"), _("Rush")),
]


def get_countries():
    items = map(lambda country: (country.alpha_2, country.name), geo.get_countries())
    items.insert(0, ("", ""))
    return items
