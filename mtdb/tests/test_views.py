import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User

from mtdb.models import Location, Gym, Review, Like
from test_base import BaseTestCase

class ViewsTestCase(BaseTestCase):

    def setUp(self):

        super().setUp()

        self.client = Client()

        user = User.objects.get(username='test_user')
        self.client.force_login(user)

    # test GET responses
    def test_index(self):
        
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["gyms"].count(), 4)

    def test_about(self):
        
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)

    def test_trip_calc(self):

        response = self.client.get("/trip_calc/")
        self.assertEqual(response.status_code, 200)

    def test_detail(self):

        gym = Gym.objects.get(name='Gym 1')
        url = gym.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_review_get(self):

        response = self.client.get("/review/")
        self.assertEqual(response.status_code, 200)

    def test_review_post(self):
        '''
        Successful post request on review page form
        '''

        response = self.client.post("/review/", {
            'gym': 1, 
            'content': 'review content',
            'session_type': 'group', 
            'start_date': datetime.date.today(), 
            'end_date': datetime.date.today(), 
            'rating_training': 1, 
            'rating_facility': 2, 
            'rating_location': 3, 
            'rating_cost': 4, 
            'rating_overall': 5,
            'images-TOTAL_FORMS': 1,
            'images-INITIAL_FORMS': 0,
            'images-MIN_NUM_FORMS': 0,
            'images-MAX_NUM_FORMS': 1
        })

        self.assertEqual(response.url, "/")

