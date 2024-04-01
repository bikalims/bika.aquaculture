from bika.lims import api
from bika.aquaculture.config import _
from senaite.impress.adapters import ActionProvider


class DownloadPDFActionProvider(ActionProvider):
    """Custom action provider to download the report PDF directly
    """
    def __init__(self, view, context, request):
        super(DownloadPDFActionProvider, self).__init__(view, context, request)
        self.title = _("Download the generated PDF to your computer")
        self.text = "<i class='fas fa-file-download'></i>"
        self.name = "impress_download_pdf"
        self.context_url = api.get_url(self.context)
        self.url = "{}/{}".format(self.context_url, self.name)
        self.modal = False  # bypass modal and POST directly to the URL

    def available(self):
        return self.view.get_allow_pdf_download() and self.is_post_mail()

    def is_post_mail(self):
        uids = filter(api.is_uid, self.request.get("items", "").split(","))
        if uids:
            postal_mail = api.get_object(uids[0]).getClient().PostalMail
            return postal_mail
        return False
