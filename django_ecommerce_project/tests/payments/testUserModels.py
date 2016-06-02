from django.test import TestCase
from payments.models import User


class UserModelsTests(TestCase):

    EMAIL_DEFAULT = "new@mail.bg"

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User(name="Username", email=cls.EMAIL_DEFAULT)
        cls.test_user.save()

    def test_user_to_string_return_email(self):
        self.assertEqual(str(self.test_user), self.EMAIL_DEFAULT)

    def test_get_user_by_id(self):
        self.assertEqual(User.get_user_by_id(1), self.test_user)

    def test_create_user_stores_in_data(self):
        new_user =  User.create(name="dummy", email="dummy@mail.bg", last_4_digits="4444", stripe_id="22", password="secret_password")
        self.assertEqual(User.objects.get(email="dummy@mail.bg"), new_user)

    def test_user_allready_exist_throw_Intergrity_Error(self):
        from django.db import IntegrityError
        self.assertRaises(IntegrityError, User.create,"Username", self.EMAIL_DEFAULT, "4444", "22", "secret_password")
