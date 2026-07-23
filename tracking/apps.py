from django.apps import AppConfig


class TrackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracking'

    def ready(self):
        import os

        print(
            "RUN_MAIN =",
            os.environ.get("RUN_MAIN")
        )

        if os.environ.get("RUN_MAIN") == "true":

            print("Starting Scheduler")

            from .scheduler import start

            start()