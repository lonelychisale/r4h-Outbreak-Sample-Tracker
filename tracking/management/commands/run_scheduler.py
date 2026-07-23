from django.core.management.base import BaseCommand

from tracking.scheduler import start


class Command(BaseCommand):

    help = "Start APScheduler"

    def handle(self, *args, **options):

        self.stdout.write(
            self.style.SUCCESS(
                "Starting Scheduler..."
            )
        )

        start()

        import time

        while True:
            time.sleep(60)