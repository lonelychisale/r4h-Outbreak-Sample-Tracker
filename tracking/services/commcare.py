import requests

from django.conf import settings
from tracking.models import CommCareSample
from datetime import datetime,timedelta

def fetch_cases():

    yesterday = (
        datetime.utcnow() - timedelta(days=1)
    ).strftime("%Y-%m-%dT%H:%M:%S")

    url = (
        f"https://www.commcarehq.org/a/"
        f"{settings.COMMCARE_DOMAIN}/api/v0.5/case/"
    )

    response = requests.get(
        url,
        params={
            "type": "Sample",
            "limit": 1000,
            "indexed_on_start": yesterday
        },
        auth=(
            settings.COMMCARE_USERNAME,
            settings.COMMCARE_API_KEY
        ),
        timeout=120
    )

    response.raise_for_status()

    return response.json()



def clean_date(value):

    if value is None:
        return None

    value = str(value).strip()

    if value.lower() in [
        "",
        "unknown",
        "none",
        "null"
    ]:
        return None

    try:
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()

    except Exception:
        return None


def import_commcare_samples():

    data = fetch_cases()

    created = 0
    updated = 0
    skipped = 0

    for case in data["objects"]:

        props = case.get("properties", {})

        sample_barcode = props.get("sample_barcode")

        # Skip records that cannot be matched to USSD
        if not sample_barcode:
            skipped += 1
            continue

        picked_by = (
            props.get("opened_by_username")
            or props.get("username")
        )

        delivered_by = (
            props.get("delivered_to_molecular_lab_by")
            or props.get("result_delivered_by")
        )

        obj, is_created = CommCareSample.objects.update_or_create(

            case_id=case["case_id"],

            defaults={

                # Matching fields
                "sample_barcode": sample_barcode,
                "tracking_number":
                    props.get("tracking_number"),

                # Patient fields
                "patient_id":
                    props.get("patient_id"),

                "patient_name":
                    props.get("patient_name"),


                # Location
                "district":
                    props.get("district"),

                "facility_name":
                    props.get("facility_name"),


                # Test
                "test_requested":
                    props.get("test_requested"),

                "sample_status":
                    props.get("sample_status"),

                "lab_name":
                    props.get("lab_name"),

                "result":
                    props.get("result"),

                # Courier fields
                "picked_by":
                    picked_by,

                "delivered_by":
                    delivered_by,

                # Dates
                "date_sample_collected_from_patient":
                    clean_date(
                        props.get(
                            "date_sample_collected_from_patient"
                        )
                    ),

                "date_sample_picked_up_by_courier":
                    clean_date(
                        props.get(
                            "date_sample_picked_up_by_courier"
                        )
                    ),

                "date_sample_delivered_to_molecular_lab":
                    clean_date(
                        props.get(
                            "date_sample_delivered_to_molecular_lab"
                        )
                    ),

                "date_result_delivered_to_facility":
                    clean_date(
                        props.get(
                            "date_result_delivered_to_facility"
                        )
                    ),
            }
        )

        if is_created:
            created += 1
        else:
            updated += 1

    print(f"Created: {created}")
    print(f"Updated: {updated}")
    print(f"Skipped: {skipped}")