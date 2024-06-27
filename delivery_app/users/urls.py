from django.urls import path
from .views import UserRegistrationView, UserLoginView, FaceImageUploadView, IDCardImageUploadView
from .views import VerificationRequestView, ManualVerificationView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload/face/', FaceImageUploadView.as_view(), name='upload_face'),
    path('upload/id/', IDCardImageUploadView.as_view(), name='upload_id'),
    path('verify/', VerificationRequestView.as_view(), name='verify'),
    path('manual-verify/<int:pk>/', ManualVerificationView.as_view(), name='manual_verify'),
]
