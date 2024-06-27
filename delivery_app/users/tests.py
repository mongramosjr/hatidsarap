from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import HatidSarapUser, FaceImage, IDCardImage, VerificationRequest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'user_type': 'customer'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(HatidSarapUser.objects.filter(username='testuser').exists())

    def test_user_login(self):
        HatidSarapUser.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class ImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = HatidSarapUser.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.face_upload_url = reverse('users:upload_face')
        self.id_upload_url = reverse('users:upload_id')

        self.base_dir = settings.BASE_DIR

    def test_face_image_upload(self):
        file_path = os.path.join(self.base_dir, 'face.jpg')
        
        with open(file_path, 'rb') as image:
            data = {
                'image': SimpleUploadedFile('id_card_image.jpg', image.read(), content_type='image/jpeg')
            }
            response = self.client.post(self.face_upload_url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertTrue(FaceImage.objects.filter(user=self.user).exists())
            self.assertEqual(IDCardImage.objects.count(), 1)
            self.assertEqual(IDCardImage.objects.get().user, user)

    def test_id_card_image_upload(self):
        image = SimpleUploadedFile("id.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(self.id_upload_url, {'image': image})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(IDCardImage.objects.filter(user=self.user).exists())

    
class VerificationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = HatidSarapUser.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.verify_url = reverse('users:verify')
        self.manual_verify_url = reverse('users:manual_verify', kwargs={'pk': 1})

        self.base_dir = settings.BASE_DIR

    def test_verification_request(self):
        # Upload face and ID images first
        face_path = os.path.join(self.base_dir, 'face.jpg')
        id_path = os.path.join(self.base_dir, 'id.jpg')
        
        with open(face_path, 'rb') as face_image, open(id_path, 'rb') as id_image:
            FaceImage.objects.create(user=self.user, image=SimpleUploadedFile('face_image.jpg', face_image.read(), content_type='image/jpeg'))
            IDCardImage.objects.create(user=self.user, image=SimpleUploadedFile('id_card_image.jpg', id_image.read(), content_type='image/jpeg'))


        response = self.client.post(self.verify_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(VerificationRequest.objects.filter(user=self.user).exists())

    def test_verification_request_without_images(self):
        response = self.client.post(self.verify_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_manual_verification(self):
        # Create a verification request first
        verification_request = VerificationRequest.objects.create(user=self.user)

        # Create an admin user
        admin_user = HatidSarapUser.objects.create_user(username='admin', password='adminpass', is_staff=True)
        self.client.force_authenticate(user=admin_user)

        response = self.client.patch(self.manual_verify_url, {'status': 'approved'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh the user instance from the database
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)

    def test_manual_verification_invalid_status(self):
        # Create a verification request first
        verification_request = VerificationRequest.objects.create(user=self.user)

        # Create an admin user
        admin_user = HatidSarapUser.objects.create_user(username='admin', password='adminpass', is_staff=True)
        self.client.force_authenticate(user=admin_user)

        response = self.client.patch(self.manual_verify_url, {'status': 'invalid_status'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TokenRefreshTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = HatidSarapUser.objects.create_user(username='testuser', password='testpass123')
        self.login_url = reverse('users:login')
        self.refresh_url = reverse('users:token_refresh')

    def test_token_refresh(self):
        # First, log in to get the tokens
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass123'})
        refresh_token = response.data['refresh']

        # Then, use the refresh token to get a new access token
        response = self.client.post(self.refresh_url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
