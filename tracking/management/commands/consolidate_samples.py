from django.core.management.base import BaseCommand

from tracking.services.merge import (
    consolidate_samples
)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        self.stdout.write(
            "Consolidating records..."
        )

        consolidate_samples()

        self.stdout.write(
            self.style.SUCCESS(
                "Consolidation Complete"
            )
        )