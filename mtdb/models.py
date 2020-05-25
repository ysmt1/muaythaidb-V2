from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse

class Location(models.Model):
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    class Meta:
        ordering = ['country','city']

    def __str__(self):
        return f'{self.city}, {self.country}'

class Gym(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    website = models.URLField(max_length=200, default='', blank=True)
    facebook = models.URLField(max_length=200, default='', blank=True)
    instagram = models.URLField(max_length=200, default='', blank=True)

    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gym_detail', kwargs={'gym_name': self.name.replace(" ", "_")})

class Review(models.Model):
    GROUP = 'group'
    PRIVATE = 'private'
    session_choices = [(GROUP, 'Group'), (PRIVATE, 'Private')]
    rating_choices = [(1,'One'),(2,'Two'),(3,'Three'),(4,'Four'),(5,'Five')]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(default=now)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    session_type = models.CharField(max_length=200, choices=session_choices, default=None)
    training_length = models.IntegerField(default=0)
    rating_training = models.IntegerField(choices=rating_choices, default=None)
    rating_facility = models.IntegerField(choices=rating_choices, default=None)
    rating_location = models.IntegerField(choices=rating_choices, default=None)
    rating_cost = models.IntegerField(choices=rating_choices, default=None)
    rating_overall = models.IntegerField(choices=rating_choices, default=None)

    @property
    def get_training_length(self):
        if self.start_date and self.end_date:
            duration = self.end_date - self.start_date
            return int(duration.days)
        return 0

    def __str__(self):
        return f'Review for {self.gym.name} by {self.author.username}'

    def save(self, *args, **kwargs):
        self.training_length = self.get_training_length
        super(Review, self).save(*args, **kwargs)
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    liked = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} has liked {self.review.author.username}'s review for {self.review.gym.name} - ID {self.review.id}"

def gym_img_path(instance, filename):
    return f'{instance.gym.name}/{filename}'

class GymImage(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=gym_img_path)

    def __str__(self):
        return f'{self.image.name}'

def review_img_path(instance, filename):
    return f'{instance.review.gym.name}/{instance.review.author.username}/{instance.review.id}/{filename}'

class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=review_img_path, blank=True, null=True)

    def __str__(self):
        return f'{self.image.name}'

    def get_filename(self):
        if self.image:
            return self.image.name.split('/')[-1]
        return None
