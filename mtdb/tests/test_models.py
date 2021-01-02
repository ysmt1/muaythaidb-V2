from mtdb.models import Location, Gym, Review, Like
from mtdb.tests.test_base import BaseTestCase

class ModelsTestCase(BaseTestCase):

    def setUp(self):

        super().setUp()

    def test_get_training_length(self):
        '''
        Review.get_training_length returns the difference in days between end and start dates
        '''

        self.assertEqual(self.review_1.get_training_length, 2)
        self.assertEqual(self.review_3.get_training_length, 0)

    def test_is_long_stay(self):
        '''
        is_long_stay() returns True if the difference between start and end dates is >= 90 days
        '''

        self.assertFalse(self.review_1.is_long_stay())
        self.assertTrue(self.review_2.is_long_stay())

    def test_has_liked(self):
        '''
        Test review that has been like returns correct count
        '''

        like_count = Like.objects.filter(review=self.review_1).count()
        self.assertEqual(like_count, 1)