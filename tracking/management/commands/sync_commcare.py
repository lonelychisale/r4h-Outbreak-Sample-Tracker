from django.core.management.base import BaseCommand

from tracking.services.commcare import (
    import_commcare_samples
)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        self.stdout.write(
            "Importing CommCare Samples..."
        )

        import_commcare_samples()

        self.stdout.write(
            self.style.SUCCESS(
                "CommCare Sync Complete"
            )
        )