# from importlib import import_module

# from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

# from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestFollowView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="tester@example",
            username="tester",
            password="testpassword",
        )
        self.user2 = User.objects.create_user(
            email="tester2@example",
            username="tester2",
            password="testpassword",
        )
        self.client.force_login(self.user)

    def test_failure_post_with_empty_username(self):
        url = reverse("accounts:follow", kwargs={"slug": self.user.slug})

        response = self.client.post(url)

        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        print(response.content)
        print(response.wsgi_request)
        # messages = response.context["messages"]
        print(message)
        # self.assertContains(response, "自分をフォローすることはできません", status_code=302)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(User.objects.count(), 0)


#         self.request = HttpRequest()
#         engine = import_module(settings.SESSION_ENGINE)
#         self.request.session = engine.SessionStore()

# def test_singup_login(self):
#     user1 = authenticate(username=self.username, password=self.password)
#     user = User.objects.get(pk=self.user.pk)
#     print(dir(user))
#     login(self.request, user1)
#     print(self.request.session)
#     self.assertEqual(BACKEND_SESSION_KEY, user1.backend)
#     print(settings.AUTHENTICATION_BACKENDS)
#     print(self.request.session[BACKEND_SESSION_KEY])

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
