"""Contact and quotation request views.

Governing documents: SPEC-002 (SPEC-002-REQ-001, REQ-003, REQ-005, section 7),
ARCH-001 (12.1, 17.4, 22.3), ADR-004.
"""

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from apps.contact.forms import ContactForm
from apps.contact.integrations.smtp_email_notifier import SmtpTransactionalEmailNotifier
from apps.contact.models import RequestStatus
from apps.contact.services.contact_service import ContactService


class ContactView(FormView):
    """Public contact form (SPEC-002-REQ-001)."""

    template_name = "contact/contact.html"
    form_class = ContactForm

    def form_valid(self, form: ContactForm) -> HttpResponse:
        service = ContactService(email_notifier=SmtpTransactionalEmailNotifier())
        contact_request = service.submit(
            full_name=form.cleaned_data["full_name"],
            email=form.cleaned_data["email"],
            subject=form.cleaned_data["subject"],
            message=form.cleaned_data["message"],
            communication_type=form.cleaned_data["communication_type"],
        )
        if contact_request.status == RequestStatus.NOTIFICATION_FAILED:
            return redirect("contact:failure")
        return redirect("contact:success")


class ContactSuccessView(TemplateView):
    """Success confirmation for a submitted request (SPEC-002 section 7)."""

    template_name = "contact/success.html"


class ContactFailureView(TemplateView):
    """Controlled, user-friendly notification failure message.

    Internal implementation details are never exposed (ARCH-001 20.3).
    """

    template_name = "contact/failure.html"
