from django.test import TestCase
from django.core.exceptions import ValidationError

from users.models import User

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="test@example.com",
        )

    def test__str__(self):
        self.assertEqual(str(self.user), self.user.username)

    def test_valid_numbers(self):
        valid_numbers = ["+79991234567", "89991234567", "79991234567"]
        for number in valid_numbers:
            user = User(username=f"user_{number}", phone_number=number, email=f"user_{number}@example.com", password=f"user_{number}password")
            try:
                user.full_clean()
            except ValidationError:
                self.fail(f"ValidationError сработал для валидного номера {number}")

    def test_invalid_numbers(self):
        invalid_numbers = [
            "+71234567",    
            "+7999123456789", 
            "1234567890", 
            "+7abcdefghij",
            "+7000000000",
        ]
        for number in invalid_numbers:
            user = User(username=f"user_{number}", phone_number=number, email=f"user_{number}@example.com", password=f"user_{number}password")
            with self.assertRaises(ValidationError, msg=f"Ожидался ValidationError для {number}"):
                user.full_clean()

    def test_phone_blank_and_null(self):
        self.assertIsNone(self.user.phone_number)
