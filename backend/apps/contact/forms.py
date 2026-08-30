"""Contact and quotation request form.

Governing documents: SPEC-002 (SPEC-002-REQ-002, REQ-003, REQ-004, section 9),
ARCH-001 (15.6, 17.2, 17.3, 17.4).
"""

from typing import Any

from django import forms
from django.utils.translation import gettext_lazy as _

from apps.contact.models import CommunicationType, ContactRequest

_INVALID_CHARACTERS = {chr(code) for code in range(0x20)} - {"\t", "\n", "\r"}


def _strip_control_characters(value: str) -> str:
    """Remove control characters that are not meaningful in user text."""

    return "".join(char for char in value if char not in _INVALID_CHARACTERS)


class ContactForm(forms.ModelForm):
    """Server-side validated contact form (SPEC-002-REQ-004).

    The communication type is optional and defaults to a contact request;
    only the fields listed in SPEC-002-REQ-002 are mandatory.
    """

    communication_type = forms.ChoiceField(
        choices=CommunicationType.choices,
        required=False,
        initial=CommunicationType.CONTACT,
        label=_("Communication type"),
    )

    class Meta:
        model = ContactRequest
        fields = ["full_name", "email", "subject", "communication_type", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": _("Type your name")}),
            "email": forms.EmailInput(attrs={"placeholder": _("name@example.com")}),
            "subject": forms.TextInput(attrs={"placeholder": _("How can I help?")}),
            "message": forms.Textarea(
                attrs={"rows": 6, "placeholder": _("Write your message")}
            ),
        }
        labels = {
            "full_name": _("Full name"),
            "email": _("Email address"),
            "subject": _("Subject"),
            "communication_type": _("Communication type"),
            "message": _("Message"),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            return

        for field_name in self.errors:
            field = self.fields.get(field_name)
            if field is None:
                continue
            field.widget.attrs["aria-invalid"] = "true"
            error_id = f"{self[field_name].id_for_label}-errors"
            described_by = str(field.widget.attrs.get("aria-describedby", "")).split()
            if error_id not in described_by:
                described_by.append(error_id)
            field.widget.attrs["aria-describedby"] = " ".join(described_by)

    def clean_full_name(self) -> str:
        return self._clean_text("full_name")

    def clean_subject(self) -> str:
        return self._clean_text("subject")

    def clean_message(self) -> str:
        return self._clean_text("message")

    def clean_communication_type(self) -> str:
        value: str = self.cleaned_data["communication_type"]
        return value or CommunicationType.CONTACT

    def _clean_text(self, field_name: str) -> str:
        value: str = self.cleaned_data[field_name]
        value = _strip_control_characters(value).strip()
        if not value:
            raise forms.ValidationError(self.fields[field_name].error_messages["required"])
        return value
