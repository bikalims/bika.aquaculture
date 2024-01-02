# -*- coding: utf-8 -*-

from senaite.app.listing.ajax im AjaxListingView as ALV

class AjaxListingView(ALV):

    @set_application_json_header
    @returns_safe_json
    @inject_runtime
    def ajax_do_action_for(self):
        """Transition multiple objects

        The POST Payload needs to provide the following data:

        :uids: A list of UIDs to transition
        :transition: The transition to perform
        """

        # Get the HTTP POST JSON Payload
        payload = self.get_json()

        required = ["uids", "transition"]
        if not all(map(lambda k: k in payload, required)):
            return self.json_message("Payload needs to provide the keys {}"
                                     .format(", ".join(required)), status=400)

        uids = payload.get("uids")
        transition = payload.get("transition")

        errors = {}
        redirects = {}

        for uid in uids:
            obj = api.get_object_by_uid(uid)

            # try named workflow transition adapter first
            adapter = queryMultiAdapter(
                (self, obj, self.request),
                interface=IListingWorkflowTransition,
                name=transition)
            if adapter is None:
                # get generic workflow transition adapter
                adapter = getMultiAdapter(
                    (self, obj, self.request),
                    interface=IListingWorkflowTransition)

            # execute the transition
            adapter.do_transition(transition)

            # collect errors
            if adapter.failed:
                errors[uid] = adapter.get_error()

            # collect redirects
            redirect = adapter.get_redirect_url()
            if redirect:
                redirects[uid] = redirect

        # fetch updated folderitems
        self.contentFilter["UID"] = uids
        folderitems = self.get_folderitems()

        # prepare the response object
        data = {
            "count": len(folderitems),
            "uids": uids,
            "folderitems": folderitems,
            "errors": errors,
            "redirects": redirects,
        }

        return data
