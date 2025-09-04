from django.test import TestCase
from users.forms import UserLoginForm, UserRegistrationForm
from users.models import User

class UserLoginFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "first_name": "testname",
            "last_name": "testlastname",
            "username": "testuser",
            "email": "testemail@example.com",
            "phone_number": "+79999999999",
            "password": "testuserpassword123",
        }

    def test_form_is_valid_with_correct_data(self):
        User.objects.create_user(**self.valid_data)
        form = UserLoginForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_if_username_is_missing(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("username")
        form = UserLoginForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
    
    def test_form_invalid_if_password_is_missing(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("password")
        form = UserLoginForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

class UserRegistrationFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
             "first_name": "testname",
            "last_name": "testlastname",
            "username": "testuser",
            "email": "testemail@example.com",
            "phone_number": "+79999999999",
            "password1": "testuserpassword123",
            "password2": "testuserpassword123",
        }

    def test_form_is_valid_with_correct_data(self):
        form = UserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_if_passwords_do_not_match(self):
        invalid_data = self.valid_data.copy()
        invalid_data["password2"] = "wrongpassword"
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_invalid_if_username_is_missing(self):
        invalid_data = self.valid_data.copy()
        invalid_data.pop("username")
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_clean_phone_number_applies_cleaner(self):
        form = UserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        cleaned_phone = form.cleaned_data["phone_number"]
        self.assertTrue(cleaned_phone.startswith("+7"))
