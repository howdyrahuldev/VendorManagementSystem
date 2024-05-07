from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("user/register/", views.user_register, name="user-register"),
    path("user/login/", views.AppTokenObtainPairView.as_view(), name="user-login"),
    path('user/refresh/', views.AppTokenRefreshView.as_view(), name="login-refresh"),
    path("vendors/", views.VendorListCreate.as_view(), name="vendor-create"),
    path("vendors/<str:vendor_code>/", views.VendorListModify.as_view(), name="vendor-modify"),
    path("vendors/<str:vendor_code>/performance/", views.VendorPerformance.as_view(), name="vendor-performance"),
    path("purchase_orders/", views.POListCreate.as_view(), name="purchase-order-create"),
    path("purchase_orders/<str:po_number>/", views.POListModify.as_view(), name="purchase-order-modify"),
    path("purchase_orders/<str:po_number>/acknowledge/",
         views.POAcknowledgement.as_view(), name="purchase-order-acknowledgement"),
]
