from django.db import models


class Vendor(models.Model):
    """
    Model to represent a vendor.
    """
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=10, primary_key=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

    def __str__(self):
        return self.vendor_code


class PurchaseOrder(models.Model):
    """
    Model to represent a purchase order.
    """
    po_number = models.CharField(max_length=10, primary_key=True)
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, default="ordered")
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(null=True)
    acknowledgment_date = models.DateTimeField(null=True)


class HistoricalPerformance(models.Model):
    """
    Model to store historical performance data of vendors.
    """
    vendor = models.ForeignKey("Vendor", on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)
