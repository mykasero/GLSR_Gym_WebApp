from django.core.exceptions import ValidationError
from django.test import TestCase
from Schedule.models import Booking, Archive, Keycodes
from django.db import IntegrityError

class BookingModelTest(TestCase):
    def setUp(self):
        self.booking1 = Booking(users="User_test", users_amount=0, 
                                start_hour="20:30", end_hour="21:30",
                                current_day="2025-01-20")
            
    def test_negative_users_amount_booking_validation(self):
        self.booking1.users_amount = -1
        with self.assertRaises(ValidationError):
            self.booking1.clean()
            
    def test_zero_users_amount_booking_validation(self):
        self.booking1.users_amount = 0
        with self.assertRaises(ValidationError):
            self.booking1.clean()
            
    def test_positive_users_amount_booking(self):
        self.booking1.users_amount = 4
        self.assertEqual(self.booking1.users_amount, 4,
                         f"Test1 for positive value failed \
                             {self.booking1.users_amount} != 4")
        
        self.booking1.users_amount = 2
        self.assertEqual(self.booking1.users_amount, 2,
                         f"Test2 for positive value failed \
                             {self.booking1.users_amount} != 2")
        
        self.booking1.users_amount = 5
        self.assertEqual(self.booking1.users_amount, 5,
                         f"Test3 for positive value failed \
                             {self.booking1.users_amount} != 5")
    
    def test_negative_users_amount_booking_constraint(self):
        """Test that the booking with negative users_amount \
            cannot be saved due to the db constraints"""
        booking = Booking(users="User_test2", users_amount=-2, 
                          start_hour="20:30", end_hour="21:30",
                          current_day="2025-01-20")
        
        with self.assertRaises(IntegrityError):
            booking.save()

class ArchiveModelTest(TestCase):
    def setUp(self):
        self.archive1 = Archive(users="User_test", users_amount=0, 
                                start_hour="20:30", end_hour="21:30",
                                current_day="2025-01-20")
            
    def test_negative_users_amount_booking_validation(self):
        self.archive1.users_amount = -1
        with self.assertRaises(ValidationError):
            self.archive1.clean()
            
    def test_zero_users_amount_booking_validation(self):
        self.archive1.users_amount = 0
        with self.assertRaises(ValidationError):
            self.archive1.clean()
            
    def test_positive_users_amount_booking(self):
        self.archive1.users_amount = 4
        self.assertEqual(self.archive1.users_amount, 4,
                         f"Test1 for positive value failed \
                             {self.archive1.users_amount} != 4")
        
        self.archive1.users_amount = 2
        self.assertEqual(self.archive1.users_amount, 2,
                         f"Test2 for positive value failed \
                             {self.archive1.users_amount} != 2")
        
        self.archive1.users_amount = 5
        self.assertEqual(self.archive1.users_amount, 5,
                         f"Test3 for positive value failed\
                             {self.archive1.users_amount} != 5")
    
    def test_negative_users_amount_booking_constraint(self):
        """Test that the archived booking with negative users_amount 
            cannot be saved due to the db constraints"""
        archive = Archive(users="User_test2", users_amount=-2, 
                          start_hour="20:30", end_hour="21:30",
                          current_day="2025-01-20")
        
        with self.assertRaises(IntegrityError):
            archive.save()
            
class KeycodesModelTest(TestCase):
    def setUp(self):
        self.keycode1 = Keycodes(code="3482", code_date="2025-01-20")
    
    def test_code_not_fully_numeric_validation(self):
        self.keycode1.code = "Z2C3"
        with self.assertRaises(ValidationError):
            self.keycode1.clean()
            
    def test_code_shorter_than_4_numbers_validation(self):
        self.keycode1.code = "231"
        with self.assertRaises(ValidationError):
            self.keycode1.clean()

    def test_keycode_not_fully_numeric_constraint(self):
        """Test that the keycode not fully numeric cannot be saved 
        due to the db constraints"""
        keycode = Keycodes(code="34z2", code_date="2025-01-20")
        
        with self.assertRaises(IntegrityError):
            keycode.save()
    
    def test_keycode_shorter_than_4_constraint(self):
        """Test that the keycode shorter than 4 cannot be saved due
        to the db constraints"""
        keycode = Keycodes(code="342", code_date="2025-01-20")
        
        with self.assertRaises(IntegrityError):
            keycode.save()