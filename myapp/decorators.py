import json
from datetime import datetime
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .utilities import update_vendor_fields, update_historical_performance
from typing import Callable


def purchase_order_override_with_vendor_condition(func: Callable) -> Callable:
    """
    Decorator function to override purchase order creation/update behavior based on vendor conditions.

    Args:
        func (Callable): The view function to be decorated.

    Returns:
        Callable: Decorated view function.
    """
    def wrapper(self, request: Request, *args, **kwargs) -> Response:
        """
        Wrapper function to implement purchase order behavior override based on vendor conditions.

        Args:
            self: The class instance.
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object.
        """
        po_number = self.kwargs.get("po_number")
        vendor = self.request.data.get("vendor")
        vendor_obj = Vendor.objects.filter(vendor_code=vendor).first()

        delivery_date = self.request.data.get("delivery_date")
        items = json.loads(self.request.data.get("items"))
        quantity = self.request.data.get("quantity")
        quality_rating = self.request.data.get("quality_rating")

        if not quality_rating:
            quality_rating = None

        if self.request.method == "PUT":
            purchase_order = PurchaseOrder.objects.get(po_number=po_number)
            po_status = self.request.data.get("status")

            if purchase_order.vendor != vendor_obj:
                purchase_order.vendor = vendor_obj
                purchase_order.issue_date = datetime.now()

            purchase_order.delivery_date = delivery_date
            purchase_order.items = items
            purchase_order.quantity = quantity

            if quality_rating and po_status != "completed":
                purchase_order.quality_rating = None
                purchase_order.save()
                return Response(
                    data="Quality rating can only be given at the time of order complete.",
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

            if purchase_order.status != po_status and not vendor_obj:
                return Response(
                    data="You are trying to change status without assigning to a vendor first.",
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            elif purchase_order.status != po_status:
                if not purchase_order.acknowledgment_date:
                    return Response(
                        data="Vendor should acknowledge the PO at the first place.",
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )

                update_vendor_fields(vendor_obj)

                if po_status == "completed" and vendor_obj:
                    purchase_order.status = po_status
                    purchase_order.quality_rating = quality_rating
                    purchase_order.save()

                    update_historical_performance(vendor_obj)

                elif po_status == "completed":
                    return Response(
                        data="Status can not be completed unless a vendor is assigned.",
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                else:
                    purchase_order.status = po_status
                    purchase_order.save()
            else:
                purchase_order.save()
        elif self.request.method == "POST":
            purchase_order = self.get_serializer(data=self.request.data)
            purchase_order.is_valid(raise_exception=True)
            purchase_order.save()

        return func(self, request, *args, **kwargs)

    return wrapper
