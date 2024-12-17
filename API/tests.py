from django.test import TestCase

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.hashers import make_password

from .models import User


class TC_UserManager(TestCase):
    def setUp(self):
        self.userManager = User.objects

    def test_CreateUser_regular_login_myuser_password_123(self):
        expected_login = "myuser"
        expected_password = "123"
        expected_is_staff = False
        expected_is_superuser = False

        self.userManager.create_user(login=expected_login, password=expected_password)
        user = self.userManager.get(login=expected_login)
        salt = user.password.split("$")[2]
        actual_login = user.login
        actual_password = user.password
        actual_is_staff = user.is_staff
        actual_is_superuser = user.is_superuser

        self.assertEqual(expected_login, actual_login)
        self.assertEqual(make_password(expected_password, salt=salt), actual_password)
        self.assertEqual(expected_is_staff, actual_is_staff)
        self.assertEqual(expected_is_superuser, actual_is_superuser)

    def test_CreateUser_must_have_a_login(self):
        expected_password = "123"
        expected_exception_message = "Users must have a login"

        with self.assertRaises(ValueError) as catch:
            self.userManager.create_user(login=None, password=expected_password)

        actual_exception_message = str(catch.exception)
        self.assertEqual(expected_exception_message, actual_exception_message)

    def test_CreateUser_when_commit_is_false_is_not_commited(self):
        expected_exception_message = "User matching query does not exist."

        login = "myuser"
        password = "123"
        self.userManager.create_user(login=login, password=password, commit=False)
        with self.assertRaises(ObjectDoesNotExist) as catch:
            self.userManager.get(login=login)
        actual_exception_message = str(catch.exception)

        self.assertEqual(expected_exception_message, actual_exception_message)

    def test_CreateSuperuser_superuser_login_mysuperuser_password_123(self):
        expected_login = "mysuperuser"
        expected_password = "123"
        expected_is_staff = True
        expected_is_superuser = True

        self.userManager.create_superuser(
            login=expected_login, password=expected_password
        )
        superuser = self.userManager.get(login=expected_login)
        salt = superuser.password.split("$")[2]
        actual_login = superuser.login
        actual_password = superuser.password
        actual_is_staff = superuser.is_staff
        actual_is_superuser = superuser.is_superuser

        self.assertEqual(expected_login, actual_login)
        self.assertEqual(make_password(expected_password, salt=salt), actual_password)
        self.assertEqual(expected_is_staff, actual_is_staff)
        self.assertEqual(expected_is_superuser, actual_is_superuser)

    def test_CreateSuperuser_must_have_a_login(self):
        expected_password = "123"
        expected_exception_message = "Users must have a login"

        with self.assertRaises(ValueError) as catch:
            self.userManager.create_superuser(login=None, password=expected_password)

        actual_exception_message = str(catch.exception)
        self.assertEqual(expected_exception_message, actual_exception_message)


class TC_User(TestCase):
    pass
