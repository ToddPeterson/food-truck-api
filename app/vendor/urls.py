from django.urls import path, include
from rest_framework.routers import DefaultRouter

from vendor import views


app_name = 'vendor'

router = DefaultRouter()
router.register('vendors', views.VendorViewSet)

urlpatterns = [
    path('me/', views.ManageVendorView.as_view(), name='me'),
    path('', include(router.urls)),
]
