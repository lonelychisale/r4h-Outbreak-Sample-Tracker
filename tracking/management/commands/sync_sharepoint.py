from django.core.management.base import BaseCommand

from tracking.services.sharepoint import (
    sync_sharepoint_excel
)


class Command(BaseCommand):

    help = (
        "Sync outbreak data "
        "to SharePoint Excel"
    )

    def handle(self, *args, **kwargs):

        self.stdout.write(
            "Syncing SharePoint..."
        )

        result = sync_sharepoint_excel()

        if result is None:

            self.stdout.write(
                self.style.WARNING(
                    "Workbook locked. "
                    "Sync skipped."
                )
            )

            return

        self.stdout.write(
            self.style.SUCCESS(
                "SharePoint Updated"
            )
        )

        self.stdout.write(
            f"File URL: "
            f"{result.get('webUrl')}"
        )