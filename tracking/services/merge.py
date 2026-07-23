from datetime import datetime

from tracking.models import (
    USSDSample,
    CommCareSample,
    ConsolidatedSample
)

def consolidate_samples():

    created = 0
    updated = 0

    for ussd in USSDSample.objects.all():

        commcare = (
            CommCareSample.objects
            .filter(
                sample_barcode=ussd.tracking_number
            )
            .first()
        )

        total_hours = None

        if (
            commcare
            and ussd.date_reported
            and commcare.date_sample_delivered_to_molecular_lab
        ):

            reported = ussd.date_reported

            delivered = datetime.combine(
                commcare.date_sample_delivered_to_molecular_lab,
                datetime.min.time()
            )

            total_hours = round(
                (
                    delivered - reported.replace(
                        tzinfo=None
                    )
                ).total_seconds() / 3600,
                2
            )

        obj, is_created = (
            ConsolidatedSample.objects.update_or_create(

                Sample_id=ussd.tracking_number,
                Sample_subtype=ussd.sample,

                defaults={
                    "ussd_id": ussd.ussd_id,
                    "coc_id": ussd.coc_id,
                    "Sample_type": ussd.sample_type,
                    "Sample_subtype":
                        ussd.sample,
                    "date_of_notification":
                        ussd.date_reported,
                    "reported_by":
                        ussd.reported_by,
                    "picked_by":
                        (
                            commcare.picked_by
                            if commcare else None
                        ),

                    "pickup_location":
                        (
                            commcare.facility_name
                            if commcare else ussd.facility
                        ),

                    "district":
                        (
                            ussd.district
                            if ussd.district else None
                        ),

                    "pickup_date":
                        (
                            commcare.date_sample_picked_up_by_courier
                            if commcare else None
                        ),

                    "delivery_location":
                        (
                            commcare.lab_name
                            if commcare else None
                        ),
                     "receivedby":
                        (
                            commcare.receivedby
                            if commcare else None
                        ),
                        "receivedbyphonenumber":
                        (
                            commcare.received_by_phone_number
                            if commcare else None
                        ),

                    "delivery_date":
                        (
                            commcare.date_sample_delivered_to_molecular_lab
                            if commcare else None
                        ),
                     "total_hours":
                        total_hours,

                    "remarks":
                        (
                            commcare.sample_status
                            if commcare else ""
                        ),

                    
                }
            )
        )
       

        if is_created:
            created += 1
        else:
            updated += 1

    print(f"Created: {created}")
    print(f"Updated: {updated}")