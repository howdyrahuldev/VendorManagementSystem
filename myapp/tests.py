from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Vendor, PurchaseOrder
from django.contrib.auth.models import User


class VendorListCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_vendor_list_create_unauthenticated(self):
        url = reverse('vendor-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vendor_list_create_authenticated(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('vendor-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class VendorListModifyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            vendor_code="12345"
        )

    def test_vendor_list_modify_unauthenticated(self):
        url = reverse('vendor-modify', args=[self.vendor.vendor_code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vendor_list_modify_authenticated(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('vendor-modify', args=[self.vendor.vendor_code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class VendorPerformanceTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact",
            address="Test Address",
            vendor_code="12345"
        )

    def test_vendor_performance_unauthenticated(self):
        url = reverse('vendor-performance', args=[self.vendor.vendor_code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vendor_performance_authenticated(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('vendor-performance', args=[self.vendor.vendor_code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class POListCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_po_list_create_unauthenticated(self):
        url = reverse('purchase-order-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_po_list_create_authenticated(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('purchase-order-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class POListModifyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO123",
            vendor=None,
            delivery_date="2024-05-01",
            items=[],
            quantity=1
        )

    def test_po_list_modify_unauthenticated(self):
        url = reverse('purchase-order-modify', args=[self.purchase_order.po_number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_po_list_modify_authenticated(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('purchase-order-modify', args=[self.purchase_order.po_number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class POAcknowledgementTestCase(TestCase):
    @staticmethod
    def create_mock_vendor():
        vendor_code = "TEST123"
        name = "Test Vendor"
        contact_details = "Test Contact"
        address = "Test Address"
        # Create and return the mock Vendor object
        return Vendor.objects.create(vendor_code=vendor_code, name=name, contact_details=contact_details,
                                     address=address)

    def setUp(self):
        vendor_obj = self.create_mock_vendor()
        self.client = APIClient()
        self.purchase_order = PurchaseOrder.objects.create(
            po_number="PO123",
            vendor=vendor_obj,
            delivery_date="2024-05-01",
            items=[],
            quantity=1
        )

    def test_po_acknowledgement_unauthenticated(self):
        url = reverse('purchase-order-acknowledgement', args=[self.purchase_order.po_number])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_po_acknowledgement_authenticated(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = reverse('purchase-order-acknowledgement', args=[self.purchase_order.po_number])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
