from django.db import models


class USSDSample(models.Model):

    ussd_id = models.IntegerField(unique=True)

    region = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    facility = models.CharField(max_length=255, blank=True, null=True)

    tracking_number = models.CharField(
        max_length=100,
        db_index=True
    )

    coc_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    sample = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    sample_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    collected = models.BooleanField(default=False)

    reported_by = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    date_reported = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tracking_number} ({self.coc_id})"

class CommCareSample(models.Model):

    case_id = models.CharField(
        max_length=255,
        unique=True
    )

    sample_barcode = models.CharField(
        max_length=100,
        db_index=True,
        null=True,
        blank=True
    )

    tracking_number = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    patient_id = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    patient_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    facility_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    test_requested = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    sample_status = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    lab_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    picked_by = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    delivered_by = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    receivedby = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    receivedbyphonenumber = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    result = models.TextField(
        null=True,
        blank=True
    )

    date_sample_collected_from_patient = models.DateField(
        null=True,
        blank=True
    )

    date_sample_picked_up_by_courier = models.DateField(
        null=True,
        blank=True
    )

    date_sample_delivered_to_molecular_lab = models.DateField(
        null=True,
        blank=True
    )

    date_result_delivered_to_facility = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
class SyncLog(models.Model):

    source = models.CharField(max_length=50, unique=True)

    last_sync = models.DateTimeField(
        null=True,
        blank=True
    )

class ConsolidatedSample(models.Model):
    ussd_id = models.IntegerField(unique=False,blank=True, null=True)
    coc_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    Sample_id = models.CharField(
        max_length=100,
        unique=False,
    )

    Sample_type = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    Sample_subtype = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    date_of_notification = models.DateTimeField(
        null=True,
        blank=True
    )
    reported_by = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    picked_by = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    pickup_location = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    pickup_date = models.DateField(
        null=True,
        blank=True
    )

    delivery_location = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    receivedby = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    receivedbyphonenumber = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    delivery_date = models.DateField(
        null=True,
        blank=True
    )

    delivery_time = models.TimeField(
        null=True,
        blank=True
    )

    total_hours = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    remarks = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )