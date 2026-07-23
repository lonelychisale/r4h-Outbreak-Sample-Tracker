from apscheduler.schedulers.background import BackgroundScheduler

from django.core.management import call_command

from apscheduler.schedulers.background import (
    BackgroundScheduler
)

scheduler = BackgroundScheduler()


def sync_job():

    call_command("sync_all")


def start():

    if scheduler.running:
        return

    scheduler.add_job(
        sync_job,
        trigger="interval",
        minutes=10,
        id="outbreak_sync",
        replace_existing=True
    )

    scheduler.start()

    print("Scheduler started")