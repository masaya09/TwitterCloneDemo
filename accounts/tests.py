# from importlib import import_module

# from django.conf import settings
# from django.contrib.auth import BACKEND_SESSION_KEY, authenticate, get_user_model, login
# from django.http import HttpRequest
# from django.test import TestCase
# from django.urls import reverse

# User = get_user_model()


# class TestSignUp(TestCase):
#     def setUp(self):
#         self.username = "tester"
#         self.password = "testpassword"
#         self.user = User.objects.create_user(
#             username=self.username,
#             password=self.password,
#         )
#         self.url = reverse("accounts:signup")
#         self.request = HttpRequest()
#         engine = import_module(settings.SESSION_ENGINE)
#         self.request.session = engine.SessionStore()

#     def test_singup_login(self):
#         user1 = authenticate(username=self.username, password=self.password)
#         user = User.objects.get(pk=self.user.pk)
#         print(dir(user))
#         login(self.request, user1)
#         print(self.request.session)
#         self.assertEqual(BACKEND_SESSION_KEY, user1.backend)
#         print(settings.AUTHENTICATION_BACKENDS)
#         print(self.request.session[BACKEND_SESSION_KEY])

#     def test_signup_view(self):
#         data = {
#             "username": "tester2",
#             "email": "tester2@test.com",
#             "password": self.password,
#         }
#         response = self.client.post(self.url, data)
#         attributes = dir(response)
#         for attribute in attributes:
#             print(attribute)

#         print(response.set_cookie)
