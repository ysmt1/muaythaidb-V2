import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from mtdb.models import Location, Gym, Review, Like

class BaseTestCase(TestCase):

    def setUp(self):

        # Create test user
        user = User.objects.create_user(username='test_user', password='test_password', email='testemail@email.com')

        # Create locations
        loc_1 = Location.objects.create(city='City A', country='Country A')
        loc_2 = Location.objects.create(city='City B', country='Country B')

        # Create gyms
        gym_1 = Gym.objects.create(name='Gym 1', location=loc_1, website='https://www.gym1.com')
        gym_2 = Gym.objects.create(name='Gym 2', location=loc_2, website='https://www.gym2.com', facebook='https://www.facebook.com/gym2')
        gym_3 = Gym.objects.create(name='Gym 3', location=loc_2, website='https://www.gym3.com', facebook='https://www.facebook.com/gym3', 
                                    instagram='https://www.instagram.com/gym3')
        gym_4 = Gym.objects.create(name='Gym 4', location=loc_1)

        # Create reviews

        # Short stay
        start_date = datetime.date.today()
        end_date_s = start_date + datetime.timedelta(days=2)

        # Long stay
        end_date_l = start_date + datetime.timedelta(days=100)

        self.review_1 = Review.objects.create(author=user, gym=gym_1, content="review 1 content", start_date=start_date, end_date=end_date_s, session_type='group', 
                                        rating_training=5, rating_facility=5, rating_location=5, rating_cost=5, rating_overall=5)

        self.review_2 = Review.objects.create(author=user, gym=gym_2, content="review 2 content", start_date=start_date, end_date=end_date_l, session_type='private', 
                                        rating_training=5, rating_facility=5, rating_location=5, rating_cost=5, rating_overall=5)

        self.review_3 = Review.objects.create(author=user, gym=gym_3, content="review 3 content", session_type='private', 
                                        rating_training=5, rating_facility=5, rating_location=5, rating_cost=5, rating_overall=5)

        # Create like
        Like.objects.create(user=user, review=self.review_1, liked=True)