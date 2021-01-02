from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

from users.models import Profile
from users.tests.test_base import BaseTestCase

class ViewsTestCase(BaseTestCase):

    def setUp(self):

        super().setUp()

        self.client = Client()

    def test_register_get(self):
        
        response = self.client.get("/users/register/")

        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        
        response = self.client.post("/users/register/", {
            "username": "registered_user",
            "password1": "testpassword",
            "password2": "testpassword"
        })

        self.assertEqual(response.url, "/")
        self.assertEqual(User.objects.count(), 3)

    def test_logout(self):

        user = User.objects.get(username='test_user')
        self.client.force_login(user)

        response = self.client.get(reverse('users:logout'))

        self.assertEqual(response.status_code, 302)

    def test_admin(self):
        '''
        Admin landing page
        '''

        response = self.client.get("/admin/", follow=True)

        self.assertContains(response, 'Log in | Django site admin')

    def test_admin_login(self):

        user = User.objects.get(username='admin')
        self.client.force_login(user)

        response = self.client.get("/admin/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Site administration | Django site admin')
