from django.db import models
from django.contrib.auth.models import User
from mtdb.models import Gym

def profile_img_path(instance, filename):
    return f'profile/{instance.user.username}/{filename}'

class Profile(models.Model):
    EXPERIENCE_CHOICES = [
        (None, 'Select...'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    FIGHTER_CHOICES = [
        (None, 'Select...'),
        ('amateur', 'Amateur'),
        ('professional', 'Professional')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile/default.png', upload_to=profile_img_path)
    location = models.CharField(max_length=200, blank=True)
    experience = models.CharField(max_length=200, choices=EXPERIENCE_CHOICES, blank=True)
    fighter = models.CharField(max_length=200, choices=FIGHTER_CHOICES, blank=True)
    checkin = models.ForeignKey(Gym, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_filename(self):
        if self.image:
            return self.image.name.split('/')[-1]
        return None
