from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('create-vendor/', views.CreateVendorUserView.as_view(), name="create_vendor"),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
