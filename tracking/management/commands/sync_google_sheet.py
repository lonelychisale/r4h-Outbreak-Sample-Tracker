from django.core.management.base import BaseCommand

from tracking.services.google_sheet import (
    sync_google_sheet
)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        sync_google_sheet()

        self.stdout.write(
            self.style.SUCCESS(
                "Google Sheet Updated"
            )
        )