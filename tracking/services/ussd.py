import os
import pandas as pd
import requests

from datetime import datetime
from django.conf import settings
from requests.structures import CaseInsensitiveDict

from tracking.models import USSDSample
from django.conf import settings


def download_ussd_csv():

    url = settings.USSD_EXPORT_URL

    headers = CaseInsensitiveDict()

    headers["Accept"] = "*/*"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    headers["Cookie"] = (
        f"username={settings.USSD_USERNAME}; "
        f"password={settings.USSD_PASSWORD}"
    )

    data = {
        "type": "csv",
        "records": "all",
        "rndVal": "0.28999320348498614"
    }

    print("Downloading USSD file...")

    response = requests.post(
        url,
        headers=headers,
        data=data,
        timeout=60
    )

    response.raise_for_status()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    filename = f"sample_collection_{timestamp}.csv"

    filepath = os.path.join(
        settings.USSD_DOWNLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as f:
        f.write(response.content)

    print(f"Downloaded: {filepath}")

    cleanup_old_files(
    settings.BASE_DIR / "downloads" / "ussd"
     )

    return filepath


import os
import glob


def cleanup_old_files(download_folder):

    files = glob.glob(
        os.path.join(download_folder, "*.csv")
    )

    if not files:
        return

    latest_file = max(
        files,
        key=os.path.getmtime
    )

    for file in files:

        if file != latest_file:

            os.remove(file)

            print(
                f"Deleted: {os.path.basename(file)}"
            )

    print(
        f"Keeping: {os.path.basename(latest_file)}"
    )



import pandas as pd

def preview_csv(filepath):

    df = pd.read_csv(filepath)

    print(df.columns.tolist())

    return df.head()


count_before = USSDSample.objects.count()

# import happens

count_after = USSDSample.objects.count()

new_records = count_after - count_before

print(f"New records added: {new_records}")

def import_ussd_csv(filepath):

    df = pd.read_csv(filepath)

    imported = 0
    created = 0
    updated = 0

    for _, row in df.iterrows():

        obj, is_created = USSDSample.objects.update_or_create(
            ussd_id=row["id"],
            defaults={
                "region": row["region"],
                "district": row["district"],
                "facility": row["facility_or_epa"],
                "tracking_number": str(row["sample_id"]),
                "coc_id": str(row["coc_id"]),
                "sample": row["sample_name"],
                "sample_type": row["sample_type"],
                "collected": False,
                "reported_by": str(row["reporter"]),
                "date_reported": row["date"],
            }
        )

        imported += 1

        if is_created:
            created += 1
        else:
            updated += 1

    print(f"Imported: {imported}")
    print(f"Created: {created}")
    print(f"Updated: {updated}")