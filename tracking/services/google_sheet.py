import gspread

from google.oauth2.service_account import Credentials

from django.conf import settings

from tracking.models import ConsolidatedSample


HEADERS = [
    "ussd_id",
    "coc_id",
    "Sample_id",
    "Sample_type",
    "Sample_subtype",
    "date_of_notification",
    "picked_by",
    "pickup_location",
    "district",
    "pickup_date",
    "delivery_location",
    "receivedby",
    "receivedbyphonenumber",
    "delivery_date",
    "delivery_time",
    "total_hours",
    "remarks",
    "updated_at",
]


def get_worksheet():

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = Credentials.from_service_account_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=scopes
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(
        settings.GOOGLE_SHEET_ID
    )

    worksheet = spreadsheet.worksheet(
        settings.GOOGLE_WORKSHEET_NAME
    )

    return worksheet


def sync_google_sheet():

    worksheet = get_worksheet()

    records = ConsolidatedSample.objects.all().order_by(
        "Sample_id"
    )

    data = [HEADERS]

    for record in records:

        data.append([

            record.ussd_id or "",

            record.coc_id or "",

            record.Sample_id or "",

            record.Sample_type or "",

            record.Sample_subtype or "",

            (
                record.date_of_notification.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if record.date_of_notification
                else ""
            ),

            record.picked_by or "",

            record.pickup_location or "",

            record.district or "",

            (
                record.pickup_date.strftime(
                    "%Y-%m-%d"
                )
                if record.pickup_date
                else ""
            ),

            record.delivery_location or "",

            record.receivedby or "",

            record.receivedbyphonenumber or "",

            (
                record.delivery_date.strftime(
                    "%Y-%m-%d"
                )
                if record.delivery_date
                else ""
            ),

            (
                record.delivery_time.strftime(
                    "%H:%M:%S"
                )
                if record.delivery_time
                else ""
            ),

            (
                float(record.total_hours)
                if record.total_hours is not None
                else ""
            ),

            record.remarks or "",

            (
                record.updated_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if record.updated_at
                else ""
            ),

        ])

    worksheet.clear()

    worksheet.update(
        "A1",
        data
    )

    print(
        f"Successfully synced "
        f"{len(records)} records"
    )