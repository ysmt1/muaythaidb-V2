from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput
from .models import Profile
from mtdb.models import Gym

class MyImageWidget(ClearableFileInput):
    template_name = "users/widgets/fileinput_template.html"

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    checkin = forms.ModelChoiceField(Gym.objects.all(), required=False, empty_label="Select Gym")

    class Meta:
        model = Profile
        fields = ['location', 'experience', 'fighter', 'checkin', 'image']
        widgets = {
            'image': MyImageWidget
        }