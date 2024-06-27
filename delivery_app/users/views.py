from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import HatidSarapUser, FaceImage, IDCardImage, VerificationRequest
from .serializers import UserSerializer, FaceImageSerializer, IDCardImageSerializer, VerificationRequestSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = HatidSarapUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class FaceImageUploadView(generics.CreateAPIView):
    queryset = FaceImage.objects.all()
    serializer_class = FaceImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IDCardImageUploadView(generics.CreateAPIView):
    queryset = IDCardImage.objects.all()
    serializer_class = IDCardImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VerificationRequestView(generics.CreateAPIView):
    queryset = VerificationRequest.objects.all()
    serializer_class = VerificationRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Check if user has uploaded both face and ID card images
        user = self.request.user
        if not hasattr(user, 'faceimage') or not hasattr(user, 'idcardimage'):
            return Response({"error": "Please upload both face and ID card images before requesting verification."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Perform automatic verification (you can implement your own logic here)
        # For demonstration purposes, we'll just set it to pending
        serializer.save(user=user, status='pending')

        # In a real-world scenario, you would implement face comparison logic here
        # and update the status accordingly


class ManualVerificationView(generics.UpdateAPIView):
    queryset = VerificationRequest.objects.all()
    serializer_class = VerificationRequestSerializer
    permission_classes = [IsAuthenticated]  # You might want to add a custom permission for admins

    def update(self, request, *args, **kwargs):
        verification_request = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in ['approved', 'rejected']:
            return Response({"error": "Invalid status. Choose 'approved' or 'rejected'."}, status=status.HTTP_400_BAD_REQUEST)

        verification_request.status = new_status
        verification_request.save()

        if new_status == 'approved':
            verification_request.user.is_verified = True
            verification_request.user.save()

        return Response(self.get_serializer(verification_request).data)
