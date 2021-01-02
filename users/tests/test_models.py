from django.contrib.auth.models import User

from users.models import Profile
from users.tests.test_base import BaseTestCase

class ModelsTestCase(BaseTestCase):

    def setUp(self):

        super().setUp()
    
    def test_profile_str(self):

        user = User.objects.get(username='test_user')

        self.assertEqual(str(user.profile), "test_user's profile")

    def test_profile_creation(self):
        '''
        Profile should be made at the same time a user is created
        '''

        count = Profile.objects.count()

        self.assertEqual(count, 2)

