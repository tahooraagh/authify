from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='StrongTestPass123!'
        )

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_successful_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'AnotherStrongPass123!',
            'password2': 'AnotherStrongPass123!',
        })

        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_duplicate_email_is_rejected(self):
        response = self.client.post(reverse('register'), {
            'username': 'anotheruser',
            'email': 'TEST@example.com',
            'password': 'AnotherStrongPass123!',
            'password2': 'AnotherStrongPass123!',
        })

        self.assertRedirects(response, reverse('register'))
        self.assertFalse(User.objects.filter(username='anotheruser').exists())

    def test_successful_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'StrongTestPass123!',
        })

        self.assertRedirects(response, reverse('home'))

    def test_login_with_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'WrongPassword123!',
        })

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_registration_with_mismatched_passwords(self):
        response = self.client.post(reverse('register'), {
            'username': 'mismatchuser',
            'email': 'mismatch@example.com',
            'password': 'StrongTestPass123!',
            'password2': 'DifferentPass456!',
        })

        self.assertRedirects(response, reverse('register'))
        self.assertFalse(User.objects.filter(username='mismatchuser').exists())

    def test_home_requires_login(self):
        response = self.client.get(reverse('home'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('home')}"
        )
