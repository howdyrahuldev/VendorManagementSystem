from datetime import datetime
from django.db.models import Avg
from .models import HistoricalPerformance, PurchaseOrder


def update_vendor_fields(vendor_obj):
    """
    Update the fields of a vendor based on their purchase order history.

    Args:
        vendor_obj: The vendor object whose fields need to be updated.

    Returns:
        None
    """
    if vendor_obj:
        vendor_specific_completed_po = PurchaseOrder.objects.filter(
            vendor=vendor_obj,
            status="completed",
        ).count()

        vendor_specific_total_po = PurchaseOrder.objects.filter(
            vendor=vendor_obj,
        ).count()

        if vendor_specific_total_po:
            vendor_obj.fulfillment_rate = vendor_specific_completed_po / vendor_specific_total_po

        vendor_obj.save()

        if vendor_specific_completed_po > 0:
            vendor_specific_completed_po_on_time = PurchaseOrder.objects.filter(
                vendor=vendor_obj,
                status="completed",
                delivery_date__lte=datetime.now(),
            ).count()

            vendor_specific_total_completed_po = PurchaseOrder.objects.filter(
                vendor=vendor_obj,
                status="completed",
            ).count()

            vendor_obj.on_time_delivery_rate = vendor_specific_completed_po_on_time / vendor_specific_total_completed_po
            vendor_obj.quality_rating_avg = PurchaseOrder.objects.filter(
                vendor=vendor_obj,
                status="completed",
            ).exclude(quality_rating=None).aggregate(starsAvg=Avg("quality_rating"))['starsAvg']

        vendor_obj.save()


def update_historical_performance(vendor_obj):
    """
    Update the historical performance record of a vendor.

    Args:
        vendor_obj: The vendor object whose historical performance needs to be updated.

    Returns:
        None
    """
    if vendor_obj:
        historical_performance, _ = HistoricalPerformance.objects.get_or_create(vendor=vendor_obj)
        historical_performance.on_time_delivery_rate = vendor_obj.on_time_delivery_rate
        historical_performance.quality_rating_avg = vendor_obj.quality_rating_avg
        historical_performance.average_response_time = vendor_obj.average_response_time
        historical_performance.fulfillment_rate = vendor_obj.fulfillment_rate
        historical_performance.save()
