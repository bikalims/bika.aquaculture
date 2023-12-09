# -*- coding: utf-8 -*-

from bika.aquaculture.config import _
from senaite.core.api import geo

BATCH_PRIORITY = [
    (_("routine"), _("Routine")),
    (_("rush"), _("Rush")),
]

SEXES = [
    (_(""), _("")),
    (_("male"), _("Male")),
    (_("female"), _("Female")),
]


def get_countries():
    items = map(lambda country: (country.alpha_2, country.name), geo.get_countries())
    items.insert(0, ("", ""))
    return items


def get_ages():
    items = map(lambda age: (str(age), age), range(0, 100))
    items.insert(0, ("", ""))
    return items
