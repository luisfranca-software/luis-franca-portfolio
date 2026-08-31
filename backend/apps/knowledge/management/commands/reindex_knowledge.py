"""Management command to reindex Knowledge Base documents.

Governing documents: SPEC-004 §41.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

from apps.knowledge.integrations.openai_embedding_provider import OpenAIEmbeddingProvider
from apps.knowledge.models import KnowledgeDocument
from apps.knowledge.services.embedding_provider import EmbeddingError
from apps.knowledge.services.indexing import IndexingService


class Command(BaseCommand):
    """Reindex KnowledgeDocument records using the production OpenAI provider."""

    help = "Reindex Knowledge Base documents"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--slug",
            type=str,
            help="Reindex only the document with the given slug.",
        )
        parser.add_argument(
            "--language",
            type=str,
            help="Reindex documents with the given language code.",
        )
        parser.add_argument(
            "--category",
            type=str,
            help="Reindex documents with the given category.",
        )

    def handle(self, *args, **options) -> None:
        try:
            provider = self._create_provider()
        except EmbeddingError as exc:
            raise CommandError(f"Embedding provider is not configured: {exc}") from exc

        service = IndexingService(provider)

        queryset = KnowledgeDocument.objects.all()
        if options["slug"]:
            queryset = queryset.filter(slug=options["slug"])
        if options["language"]:
            queryset = queryset.filter(language=options["language"])
        if options["category"]:
            queryset = queryset.filter(category=options["category"])

        total = queryset.count()
        self.stdout.write(f"Reindexing {total} document(s)...")

        success = 0
        failure = 0
        for document in queryset:
            try:
                service.index_document(document)
                success += 1
                self.stdout.write(self.style.SUCCESS(f"Indexed: {document}"))
            except EmbeddingError as exc:
                failure += 1
                self.stderr.write(self.style.ERROR(f"Failed: {document}"))
                self.stderr.write(str(exc))

        self.stdout.write(f"Done. Success: {success}, Failure: {failure}, Total: {total}")

    def _create_provider(self) -> OpenAIEmbeddingProvider:
        """Return the production OpenAI embedding provider.

        Never falls back to a test provider.
        """
        return OpenAIEmbeddingProvider()
