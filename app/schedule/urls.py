from django.urls import path, include
from rest_framework.routers import DefaultRouter

from schedule import views

app_name = 'schedule'

router = DefaultRouter()
router.register('locations', views.LocationViewSet)

urlpatterns = [
    path('', include(router.urls))
]
