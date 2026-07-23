from django.core.management.base import BaseCommand

from django.core.management.base import BaseCommand

from tracking.services.ussd import (
    download_ussd_csv,
    import_ussd_csv
)
class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        self.stdout.write("Downloading file...")

        filepath = download_ussd_csv()

        self.stdout.write("Importing data...")

        import_ussd_csv(filepath)

        self.stdout.write(
            self.style.SUCCESS(
                "USSD Sync Complete"
            )
        )