"""Integration tests for the Django i18n foundation (ADR-002).

Brazilian Portuguese must be supported using the existing Django i18n
foundation; English is the canonical source language.
"""

from django.test import Client
from django.utils import translation

from apps.contact.forms import ContactForm
from apps.contact.models import CommunicationType


def test_form_labels_are_translated_to_pt_br() -> None:
    with translation.override("pt-br"):
        form = ContactForm()
        assert str(form.fields["full_name"].label) == "Nome completo"
        assert str(form.fields["email"].label) == "Endereço de e-mail"
        assert str(form.fields["subject"].label) == "Assunto"
        assert str(form.fields["message"].label) == "Mensagem"
        option_labels = dict(CommunicationType.choices)
        assert option_labels["contact"] == "Contato"
        assert option_labels["quotation"] == "Solicitação de orçamento"


def test_english_is_the_default_language() -> None:
    content = Client().get("/contact/").content.decode()

    assert "Contact" in content
    assert "Full name" in content


def test_pt_br_page_renders_translated_content() -> None:
    content = Client().get("/contact/", HTTP_ACCEPT_LANGUAGE="pt-br").content.decode()

    assert "Contato" in content
    assert "Nome completo" in content
    assert "Enviar mensagem" in content


def test_pt_br_success_page_is_translated() -> None:
    response = Client().get("/contact/success/", HTTP_ACCEPT_LANGUAGE="pt-br")

    assert "Mensagem enviada" in response.content.decode()
