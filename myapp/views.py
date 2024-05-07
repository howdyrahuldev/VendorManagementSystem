from datetime import datetime
from typing import Any
from django.db.models import Avg, F
from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Vendor, PurchaseOrder
from .decorators import purchase_order_override_with_vendor_condition
from .serializers import (
    AppTokenObtainPairSerializer,
    AppTokenRefreshSerializer,
    PurchaseOrderAcknowledgeSerializer,
    PurchaseOrderSerializer,
    PurchaseOrderCreateSerializer,
    PurchaseOrderUpdateSerializer,
    VendorCreateUpdateSerializer,
    VendorListSerializer,
    VendorPerformanceSerializer,
)
from .forms import CreateUserForm


class VendorListCreate(generics.ListCreateAPIView):
    """
    List and create vendors.

    GET: Retrieve a list of vendors.
    POST: Create a new vendor.
    """
    permission_classes = [IsAuthenticated, ]
    queryset = Vendor.objects.all()

    def get_serializer_class(self) -> Any:
        if self.request.method == 'POST':
            return VendorCreateUpdateSerializer
        return VendorListSerializer


class VendorListModify(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a vendor by its code.

    GET: Retrieve a vendor by its code.
    PUT: Update a vendor by its code.
    DELETE: Delete a vendor by its code.
    """
    permission_classes = [IsAuthenticated, ]
    queryset = Vendor.objects.all()

    def get_serializer_class(self) -> Any:
        if self.request.method == 'PUT':
            return VendorCreateUpdateSerializer
        return VendorListSerializer

    lookup_field = "vendor_code"


class VendorPerformance(generics.RetrieveAPIView):
    """
    Retrieve vendor performance by its code.

    GET: Retrieve vendor performance by its code.
    """
    permission_classes = [IsAuthenticated, ]
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_field = "vendor_code"


class POListCreate(generics.ListCreateAPIView):
    """
    List and create purchase orders.

    GET: Retrieve a list of purchase orders.
    POST: Create a new purchase order.
    """
    permission_classes = [IsAuthenticated, ]
    queryset = PurchaseOrder.objects.all()

    def get_serializer_class(self) -> Any:
        if self.request.method == 'POST':
            return PurchaseOrderCreateSerializer
        return PurchaseOrderSerializer

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        vendor = self.request.GET.get("vendor", None)
        data = list(PurchaseOrder.objects.values())
        if vendor:
            data = list(PurchaseOrder.objects.values().filter(vendor=vendor))
        return Response(data=data, status=status.HTTP_200_OK)

    @purchase_order_override_with_vendor_condition
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return Response(status=status.HTTP_201_CREATED)


class POListModify(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a purchase order by its number.

    GET: Retrieve a purchase order by its number.
    PUT: Update a purchase order by its number.
    DELETE: Delete a purchase order by its number.
    """
    permission_classes = [IsAuthenticated, ]
    queryset = PurchaseOrder.objects.all()

    def get_serializer_class(self) -> Any:
        if self.request.method == 'PUT':
            return PurchaseOrderUpdateSerializer
        return PurchaseOrderSerializer

    lookup_field = "po_number"

    @purchase_order_override_with_vendor_condition
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return Response(status=status.HTTP_200_OK)


class POAcknowledgement(generics.RetrieveAPIView):
    """
    Acknowledge a purchase order by its number.

    POST: Acknowledge a purchase order by its number.
    """
    permission_classes = [IsAuthenticated, ]
    queryset = PurchaseOrder.objects.all()

    def get_serializer_class(self) -> Any:
        if self.request.method == 'POST':
            return PurchaseOrderAcknowledgeSerializer
        return PurchaseOrderSerializer

    lookup_field = "po_number"

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Acknowledge a purchase order by its number.

        Updates the purchase order status to "acknowledged" and sets the acknowledgment date.
        If the vendor is not assigned, returns a 406 response.
        If the purchase order is already acknowledged, returns a 406 response.
        Otherwise, updates the purchase order, calculates the average response time, and updates the vendor.
        """
        po_number = self.kwargs.get("po_number")

        purchase_order = PurchaseOrder.objects.get(po_number=po_number)

        vendor = purchase_order.vendor

        if not vendor:
            return Response(data="Must assigned to be a vendor.", status=status.HTTP_406_NOT_ACCEPTABLE)

        if purchase_order.acknowledgment_date:
            return Response(data="Already acknowledged.", status=status.HTTP_406_NOT_ACCEPTABLE)

        purchase_order.status = "acknowledged"
        purchase_order.acknowledgment_date = datetime.now()
        purchase_order.save()

        result = PurchaseOrder.objects.filter(vendor=vendor).annotate(
            duration=F("acknowledgment_date") - F("issue_date")
        ).aggregate(
            avg_duration=Avg("duration")
        )

        vendor_update = Vendor.objects.get(vendor_code=vendor)
        if result['avg_duration']:
            vendor_update.average_response_time = result['avg_duration'].total_seconds()
        else:
            vendor_update.average_response_time = None
        vendor_update.save()

        return Response(status=status.HTTP_200_OK)


class AppTokenObtainPairView(TokenObtainPairView):
    serializer_class = AppTokenObtainPairSerializer


class AppTokenRefreshView(TokenRefreshView):
    serializer_class = AppTokenRefreshSerializer


def user_register(request: Request) -> Any:
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    context = {"register_form": form}
    return render(request, "users/register.html", context=context)
