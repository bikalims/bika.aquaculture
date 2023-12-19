# -*- coding: utf-8 -*-

from Products.Archetypes.public import DisplayList
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory

from bika.aquaculture.config import _
from bika.lims import api
from senaite.core.api import geo


@provider(IVocabularyFactory)
def getUsers(context, roles, allow_empty=True):
    """ Present a DisplayList containing users in the specified
        list of roles
    """
    pairs = allow_empty and [['', '']] or []
    if not context:
        return DisplayList(pairs)

    mtool = api.get_tool('portal_membership')
    users = mtool.searchForMembers(roles=roles)
    for user in users:
        uid = user.getId()
        fullname = user.getProperty('fullname')
        if not fullname:
            fullname = uid
        pairs.append((uid, fullname))
    pairs.sort(lambda x, y: cmp(x[1], y[1]))
    return DisplayList(pairs)


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
