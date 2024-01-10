# -*- coding: utf-8 -*-

from string import Template
from collections import OrderedDict

from Products.CMFPlone.utils import safe_unicode
from Products.PlonePAS.plugins.ufactory import PloneUser
from Products.PlonePAS.tools.memberdata import MemberData
from zope.interface import implementer

from bika.aquaculture.config import _
from bika.lims import api
from bika.lims.api.mail import compose_email
from bika.lims.api.mail import is_valid_email_address
from bika.lims.interfaces import IContact
from bika.lims.utils import get_link
from bika.lims.utils import get_link_for
from senaite.app.listing.adapters.workflow import ListingWorkflowTransition
from senaite.app.listing.interfaces import IListingWorkflowTransition
from senaite.core.catalog import SAMPLE_CATALOG


@implementer(IListingWorkflowTransition)
class SampleReceiveWorkflowTransition(ListingWorkflowTransition):
    """Adapter to execute the workflow transition "receive" for samples
    """
    def __init__(self, view, context, request):
        super(SampleReceiveWorkflowTransition, self).__init__(
            view, context, request)
        self.back_url = request.get_header("referer")

    def get_redirect_url(self):
        """Redirect after sample receive transition
        """

        self.notify_client_contacts(self.context)

        if self.is_auto_partition_required():
            # Redirect to the partitioning view
            uid = api.get_uid(self.context)
            url = "{}/partition_magic?uids={}".format(self.back_url, uid)
            return url

        if self.is_auto_print_stickers_enabled():
            # Redirect to the auto-print stickers view
            uid = api.get_uid(self.context)
            url = "{}/sticker?autoprint=1&items={}".format(self.back_url, uid)
            return url

        # return default value
        return super(SampleReceiveWorkflowTransition, self).get_redirect_url()

    def is_auto_partition_required(self):
        """Returns whether the sample needs to be partitioned
        """
        template = self.context.getTemplate()
        return template and template.getAutoPartition()

    def is_auto_print_stickers_enabled(self):
        """Returns whether the auto print of stickers on reception is enabled
        """
        setup = api.get_setup()
        return "receive" in setup.getAutoPrintStickers()

    def can_send_notification(self, sample):
        """Returns whether the batch email has been sent for received samples
        """
        batch = sample.getBatch()
        if batch.NotifiedSamplesReceived:
            return False

        query = {"getBatchUID": batch.UID(),
                 "portal_type": "AnalysisRequest",
                 "getDateReceived": {'query': '', 'range': 'min'},
                 }
        brains = api.search(query, SAMPLE_CATALOG)

        samples = batch.getAnalysisRequests()
        if len(samples) == len(brains):
            # all samples have been received
            return True

    def notify_client_contacts(self, sample):
        """Checks if all samples have been received and notifies
           client contacts by email
        """
        send = self.can_send_notification(sample)
        if send:
            batch = sample.getBatch()
            samples = batch.getAnalysisRequests()
            self.send_received_email(samples)
            batch.NotifiedSamplesReceived = True
            batch.reindexObject()
            message = _("Sent email for ")
            message = _(
                "Sent email for receiving samples for ${batch_id}",
                mapping={
                    "batch_id": api.get_id(batch),
                })
            self.context.plone_utils.addPortalMessage(message, "info")

    def send_received_email(self, samples):
        """Sends an email notification to sample's client contact if the sample
        passed in has a retest associated
        """
        try:
            email_message = self.get_invalidation_email(samples)
            host = api.get_tool("MailHost")
            host.send(email_message, immediate=True)
        except Exception as err_msg:
            batch = samples[0].getBatch()
            message = _(
                "Cannot send email for receiving samples for ${batch_id} : ${error}",
                mapping={
                    "batch_id": api.get_id(batch),
                    "error": safe_unicode(err_msg)
                })
            self.context.plone_utils.addPortalMessage(message, "warning")

    def get_invalidation_email(self, samples):
        """Returns the sample invalidation MIME Message for the sample
        """
        managers = api.get_users_by_roles("LabManager")
        contacts = []
        for sample in samples:
            if sample.getContact() not in contacts:
                contacts.append(sample.getContact())
            for cc_contact in sample.getCCContact():
                if cc_contact not in contacts:
                    contacts.append(cc_contact)
        recipients = managers + contacts
        recipients = filter(None, map(self.get_email_address, recipients))
        # Get the recipients
        recipients = list(OrderedDict.fromkeys(recipients))

        if not recipients:
            for sample in samples:
                sample_id = api.get_id(sample)
                raise ValueError("No valid recipients for {}".format(sample_id))

        # TODO: Get Batch and see if the unique batch
        batch = samples[0].getBatch()
        # Compose the email
        subject = self.context.translate(_(
            "Samples received for Batch: ${batch_id}",
            mapping={"batch_id": api.get_id(batch)}
        ))

        setup = api.get_setup()
        lab_name = setup.laboratory.Title()
        lab_email = setup.laboratory.getEmailAddress()
        lab_address = setup.laboratory.getPrintAddress()
        number_of_samples = len(samples)
        client_name = batch.getClient().Title() if batch.getClient() else ""
        batch_url = batch.absolute_url()
        client_batch_id = batch.getClientBatchID()
        body = Template(setup.ReceivedSamplesEmailBody())
        body = body.safe_substitute({
            "batch_title": get_link_for(batch, csrf=False),
            "client_batch_id": get_link(batch_url, value=client_batch_id),
            "client_name": client_name,
            "lab_name": "<br/>".join(lab_name),
            "lab_address": "<br/>".join(lab_address),
            "number_of_samples": number_of_samples,
            "recipients": ", ".join([i.getFullname() for i in contacts]),
        })

        return compose_email(from_addr=lab_email, to_addr=recipients,
                             subj=subject, body=body, html=True)

    def get_email_address(self, contact_user_email):
        """Returns the email address for the contact, member or email
        """
        if is_valid_email_address(contact_user_email):
            return contact_user_email

        if IContact.providedBy(contact_user_email):
            contact_email = contact_user_email.getEmailAddress()
            return self.get_email_address(contact_email)

        if isinstance(contact_user_email, MemberData):
            contact_user_email = contact_user_email.getUser()

        if isinstance(contact_user_email, PloneUser):
            # Try with the contact's email first
            contact = api.get_user_contact(contact_user_email)
            contact_email = self.get_email_address(contact)
            if contact_email:
                return contact_email

            # Fallback to member's email
            user_email = contact_user_email.getProperty("email")
            return self.get_email_address(user_email)

        return None
