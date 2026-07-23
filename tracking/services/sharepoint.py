from io import BytesIO

import msal
import pandas as pd
import requests

from django.conf import settings

from tracking.models import ConsolidatedSample


SITE_ID = (
    "r4hmw.sharepoint.com,"
    "9be3cce0-3385-4daa-bbe3-d47245ff8aea,"
    "43b835f7-9e31-4bbe-90e3-cb53e6d5b447"
)

DRIVE_ID = (
    "b!4Mzjm4Uzqk2749RyRf-K6vc1uEMxnr5LkOPLU-bVtEc6C-l7L9JqRZKLY3GIubLu"
)


def get_access_token():

    app = msal.ConfidentialClientApplication(
        settings.CLIENT_ID,
        authority=(
            f"https://login.microsoftonline.com/"
            f"{settings.TENANT_ID}"
        ),
        client_credential=settings.CLIENT_SECRET
    )

    result = app.acquire_token_for_client(
        scopes=[
            "https://graph.microsoft.com/.default"
        ]
    )

    if "access_token" not in result:

        raise Exception(
            result.get(
                "error_description",
                "Unable to get token"
            )
        )

    return result["access_token"]

from datetime import datetime
from io import BytesIO

import pandas as pd
import requests

from tracking.models import ConsolidatedSample

from datetime import datetime
from io import BytesIO

import pandas as pd
import requests

from tracking.models import ConsolidatedSample


def sync_sharepoint_excel():

    records = (
        ConsolidatedSample.objects
        .all()
        .order_by("date_of_notification")
    )

    data = []

    for index, record in enumerate(records, start=1):

        data.append({

            "#":
                index,

            "COC ID":
                record.coc_id,

            "Sample ID":
                record.Sample_id,

            "Sample Type":
                record.Sample_type,

            "Sample Subtype":
                record.Sample_subtype,

           
            "District":
                record.district,

            "Location":
                record.pickup_location,
            "Date Of Notification":
                                (
                                    record.date_of_notification.replace(
                                        tzinfo=None
                                    )
                                    if record.date_of_notification
                                    else None
                                ),
                
            "Picked By":
                 record.picked_by,

            "Pickup Date":
                record.pickup_date,

            "Delivery Location":
                record.delivery_location,

            "Received By":
                record.receivedby,

            "Phone Number":
                record.receivedbyphonenumber,

            "Delivery Date":
                record.delivery_date,

            "Delivery Time":
                record.delivery_time,

            "Total Hours":
                record.total_hours,

            "Remarks":
                record.remarks,

        })

    df = pd.DataFrame(data)

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        # Main worksheet
        df.to_excel(
            writer,
            sheet_name="USSD Outbreak Notifications",
            index=False
        )

        # Update Information worksheet
        update_df = pd.DataFrame([

            {
                "Item": "Last Updated",
                "Value": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            },

            {
                "Item": "Total Records",
                "Value": len(df)
            },

            {
                "Item": "Status",
                "Value": "Success"
            }

        ])

        update_df.to_excel(
            writer,
            sheet_name="Update Information",
            index=False
        )

    buffer.seek(0)

    token = get_access_token()

    upload_url = (
        f"https://graph.microsoft.com/v1.0/"
        f"drives/{DRIVE_ID}"
        f"/root:/Outbreak samples/USSD Outbreak Notifications.xlsx"
        f":/content"
    )

    response = requests.put(
        upload_url,
        headers={
            "Authorization":
                f"Bearer {token}",

            "Content-Type":
                "application/octet-stream"
        },
        data=buffer.getvalue()
    )

    print(
        "Status:",
        response.status_code
    )

    if response.status_code == 423:

        print(
            "Workbook currently locked."
        )

        print(
            "Will retry during next scheduled run."
        )

        return None

    response.raise_for_status()

    return response.json()