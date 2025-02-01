from django.core.exceptions import ValidationError
from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from Schedule.models import Keycodes, Booking
import os
from django.contrib.auth import get_user_model


# homepage view
class TestHomePageView(SimpleTestCase):
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
        
    def test_navbar_contains_name_img(self):
        response = self.client.get(reverse('home'))
        logo_path_os = os.path.join(settings.STATICFILES_DIRS[0], 'images/gym_name.png')
        logo_path_template = os.path.join(settings.STATIC_URL, 'images/gym_name.png')
        self.assertTrue(os.path.exists(logo_path_os), f"Image file not found at the specified path")
        self.assertContains(response, logo_path_template)
   
# register view  
 
# login view
class TestLoginView(TestCase):    
    def test_login_url_correct(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'Schedule/login.html')
        
    def test_login_context_has_form(self):
        response = self.client.get(reverse('login'))
        self.assertIn('form', response.context)
    
    def test_login_template_has_form(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, '<form')       
        self.assertContains(response, 'name="login"')
        self.assertContains(response, 'name="haslo"')
    
    def test_login_template_has_login_button(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, '<button type="submit" class = "btn mt-3 text-center fs-6">Login</button>')
    
    def test_login_template_has_register_link(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response,"Nie masz konta?")
        self.assertContains(response, "Zarejestruj sie")
        self.assertContains(response, '<a class="link_indv" href="/register">tutaj</a>')
        
    def test_login_template_has_forgot_password_link(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response,"Zapomniałeś hasła?")
        self.assertContains(response, "Przejdź")
        self.assertContains(response, '<a class="link_indv" href="/password_reset/">tutaj</a>')
        
# login success view 
class TestLoginSuccessView(TestCase):
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
        
    def test_login_success_unauthenticated_user_tries_entry(self):
        response = self.client.get(reverse('login_success'))
        self.assertEqual(response.status_code, 302)
    
    def test_login_success_unauthenticated_user_message(self):
        response = self.client.get(
            reverse('login_success'),
            follow=True
            )
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Aby wyświetlić strone ekranu powitalnego musisz być zalogowany')
    
    def test_login_success_uses_correct_template(self):
        response = self.client.post(
                reverse('login'),
                {'login':'Testuser1', 'haslo':'Testpassword123'},
                follow=True,
            )
        
        self.assertTemplateUsed(response, 'Schedule/login_success.html')

    def test_login_success_uses_correct_template_after_redirect(self):
        response = self.client.post(
            reverse('login_success'),
            follow = True
        )
        
        self.assertTemplateUsed(response, 'Schedule/login.html')
    
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
        
# lobby view
class TestLobbyView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Testuser1',
            password='Testpassword123',
        )
        self.keycode = Keycodes.objects.create(code="1234",code_date="2025-01-20")
        
    def test_lobby_url_correct(self):
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        
        self.assertEqual(response.status_code, 200)
    
    def test_lobby_unauthenticated_user_entry(self):
        response = self.client.get(reverse('lobby'))
        self.assertEqual(response.status_code, 302)
        
    def test_lobby_unauthenticated_user_entry_message(self):
        response = self.client.get(
            reverse('lobby'),
            follow = True
            )
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Aby wyświetlić strone poczekalni musisz być zalogowany')
        
    def test_lobby_uses_correct_template(self):
        response = self.client.post(
                reverse('login'),
                {'login':'Testuser1', 'haslo':'Testpassword123'},
                follow=True,
            )
        
        response = self.client.get(reverse('lobby'))
        
        self.assertTemplateUsed(response, 'Schedule/lobby.html')

    def test_lobby_uses_correct_template_after_redirect(self):
        response = self.client.get(
            reverse('lobby'),
            follow = True
        )
        
        self.assertTemplateUsed(response, 'Schedule/login.html')
        
    def test_lobby_contains_booking_button(self):
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        
        self.client.get(reverse('lobby'))
        
        self.assertContains(response, "Rezerwacja", status_code=200)
        
    def test_lobby_contains_current_bookings_button(self):
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        
        self.client.get(reverse('lobby'))
        
        self.assertContains(response, "Dzisiejsze rezerwacje", status_code=200)
        
    def test_lobby_contains_archive_button(self):
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        
        self.client.get(reverse('lobby'))
        
        self.assertContains(response, "Archiwum", status_code=200)
        
    def test_lobby_contains_logo(self):
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        
        self.client.get(reverse('lobby'))
        
        logo_path = os.path.join(settings.STATIC_URL, 'images/logo1.png')
        self.assertContains(response, logo_path)

#add booking here

#current bookings view
class TestCurrentBookingsView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Testuser1',
            password='Testpassword123',
        )
        
        self.keycode = Keycodes.objects.create(code="1234",code_date="2025-01-20")
        
    def test_current_bookings_url_success(self):
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        
        self.client.get(reverse('current_bookings'))
        
        self.assertEqual(response.status_code, 200)
        
    def test_current_bookings_unauthenticated_user_entry(self):
        response = self.client.get(reverse('current_bookings'))
        self.assertEqual(response.status_code, 302)
        
    def test_current_bookings_unauthenticated_user_entry_message(self):
        response = self.client.get(
            reverse('current_bookings'),
            follow = True
            )
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Aby wyświetlić strone dzisiejszych rezerwacji musisz być zalogowany')
        
    def test_current_bookings_uses_correct_template(self):
        response = self.client.post(
                reverse('login'),
                {'login':'Testuser1', 'haslo':'Testpassword123'},
                follow=True,
            )
        
        response = self.client.get(reverse('current_bookings'))
        
        self.assertTemplateUsed(response, 'Schedule/current_bookings.html')
        
        
    def test_current_bookings_empty_table(self):
        response = self.client.post(
                reverse('login'),
                {'login':'Testuser1', 'haslo':'Testpassword123'},
                follow=True,
            )

        response = self.client.get(reverse('current_bookings'))
        
        # test passed context if it's truly empty
        self.assertQuerySetEqual(response.context['context'], [])
        
        response = self.client.get(
            reverse('booking_list'),
            HTTP_HX_REQUEST='true'
            )
        
        # test if the empty table info is present
        self.assertContains(response, "Nie ma jeszcze żadnych rezerwacji")
    
    def test_current_bookings_filled_table(self):
        User.objects.create_user(
            username='Testuser2',
            password='Testpassword123',
        )
        Booking.objects.create(
            users='Testuser1', 
            users_amount=3,
            start_hour="10:30",
            end_hour="11:30",
            current_day="2025-01-30"
            )
        Booking.objects.create(
            users='Testuser2', 
            users_amount=1,
            start_hour="12:30",
            end_hour="15:30",
            current_day="2025-01-30"
            )
        
        response = self.client.post(
            reverse('login'),
            {'login':'Testuser1', 'haslo':'Testpassword123'},
            follow=True,
        )
        
        response = self.client.get(reverse('current_bookings'))
        
        # test proper response code and template load
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'Schedule/current_bookings.html')
        
        # test if two bookings were uploaded correctly
        self.assertEqual(len(response.context['context']), 2)

        # check if currently logged in users id that's being passed in context is correct
        self.assertEqual(response.context['current_user'], self.user.id)
        
        response = self.client.get(reverse('booking_list'))
        
        # check if both users bookings are in the table
        self.assertContains(response, "Testuser1")
        self.assertContains(response, "Testuser2")
    
#archive view
class TestArchiveView(TestCase):
    pass