from django.test import TestCase
from django.contrib.auth.models import User

class BaseTestCase(TestCase):

    def setUp(self):

        # Create test user
        user = User.objects.create_user(username='test_user', password='test_password', email='testemail@email.com')
        admin = User.objects.create_superuser(username='admin', password='admin_password', email='admin@email.com')
