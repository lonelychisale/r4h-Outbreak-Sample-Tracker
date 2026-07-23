from django.core.management.base import BaseCommand

from tracking.services.commcare import (
    import_commcare_samples
)
from tracking.services.ussd import (
    download_ussd_csv,
    import_ussd_csv
)

from tracking.services.merge import (
    consolidate_samples
)

from tracking.services.sharepoint import (
    sync_sharepoint_excel
)

from tracking.management.commands.consolidate_samples import consolidate_samples

from tracking.management.commands.sync_google_sheet import sync_google_sheet
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Downloading USSD file...")

        filepath = download_ussd_csv()

        self.stdout.write("Importing data...")

        import_ussd_csv(filepath)
        self.stdout.write("Ussd data imported.")
        self.stdout.write("Importing CommCare data...")
        import_commcare_samples()
        self.stdout.write("CommCare data imported.")
        self.stdout.write("Consolidating samples...")
        consolidate_samples()
        self.stdout.write("Samples consolidated.")
        self.stdout.write("Syncing Google Sheet...")
        sync_google_sheet()
        self.stdout.write("Google Sheet synced.")
        self.stdout.write("Syncing SharePoint...")
        sync_sharepoint_excel()
        self.stdout.write("SharePoint synced.")
    
        self.stdout.write(
            self.style.SUCCESS(
                "Sync Complete"
            )
        )
