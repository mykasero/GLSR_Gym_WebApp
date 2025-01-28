from django.core.exceptions import ValidationError
from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from Schedule.models import Keycodes
import os

class TestHomePage(SimpleTestCase):
    def test_homepage_url_correct(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
    def test_homepage_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'Schedule/home.html')
        
    def test_homepage_contains_login_button(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Logowanie", status_code=200)
        
    def test_homepage_contains_gallery_button(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Galeria", status_code=200)
        
    def test_homepage_contains_logo(self):
        response = self.client.get(reverse('home'))
        logo_path_os = os.path.join(settings.STATICFILES_DIRS[0], 'images/logo1.png')
        logo_path_template = os.path.join(settings.STATIC_URL, 'images/logo1.png')
        self.assertTrue(os.path.exists(logo_path_os), f"Image file not found at the specified path")
        self.assertContains(response, logo_path_template)
        
class TestLoginSuccess(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Testuser1',
            password='Testpassword123',
        )
        self.keycode = Keycodes.objects.create(code="1234",code_date="2025-01-20")
        
    def test_login_success_url_correct(self):
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        
        self.assertEqual(response.status_code, 200)
        
    def test_login_success_uses_correct_template(self):
        response = self.client.post(
                reverse('login'),
                {'login':'Testuser1', 'haslo':'Testpassword123'},
                follow=True,
            )
        
        self.assertTemplateUsed(response, 'Schedule/login_success.html')
        
    def test_login_success_contains_homepage_button(self):
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        
        self.assertContains(response, "Strona Glowna", status_code=200)
        
    def test_login_success_contains_lobby_button(self):
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        self.assertContains(response, "Lobby", status_code=200)
        
    def test_login_success_contains_logo(self):
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        
        logo_path = os.path.join(settings.STATIC_URL, 'images/logo1.png')
        self.assertContains(response, logo_path)
    
    def test_login_success_contains_message_context(self):
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Kod do skrzynki z kluczem: 1234.')
    
    def test_login_success_contains_message(self):
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        
        self.assertContains(response, 'Kod do skrzynki z kluczem: 1234.')
        self.assertContains(response, 'alert-success')