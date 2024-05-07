from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import Vendor, PurchaseOrder


class VendorCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating a vendor.
    """
    class Meta:
        model = Vendor
        fields = [
            "name",
            "contact_details",
            "address",
            "vendor_code",
        ]


class VendorListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing vendors.
    """
    class Meta:
        model = Vendor
        fields = [
            "name",
            "contact_details",
            "address",
            "vendor_code",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]


class VendorPerformanceSerializer(serializers.ModelSerializer):
    """
    Serializer for vendor performance.
    """
    class Meta:
        model = Vendor
        fields = [
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for purchase orders.
    """
    class Meta:
        model = PurchaseOrder
        fields = [
            "po_number",
            "vendor",
            "order_date",
            "delivery_date",
            "items",
            "quantity",
            "status",
            "quality_rating",
            "issue_date",
            "acknowledgment_date",
        ]


class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a purchase order.
    """
    class Meta:
        model = PurchaseOrder
        fields = [
            "po_number",
            "vendor",
            "delivery_date",
            "items",
            "quantity",
        ]


class PurchaseOrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a purchase order.
    """
    class Meta:
        model = PurchaseOrder
        fields = [
            "po_number",
            "vendor",
            "order_date",
            "delivery_date",
            "items",
            "quantity",
            "status",
            "quality_rating",
        ]


class PurchaseOrderAcknowledgeSerializer(serializers.ModelSerializer):
    """
    Serializer for acknowledging a purchase order.
    """
    class Meta:
        model = PurchaseOrder
        fields = [
        ]


class AppTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        print(token)
        return token


class AppTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        data = {'refresh': str(refresh)}
        return data
