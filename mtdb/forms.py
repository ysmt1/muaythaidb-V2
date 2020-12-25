from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Field, HTML
from crispy_forms.bootstrap import StrictButton
from users.forms import MyImageWidget
from .models import Review, Gym, ReviewImage

class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    hidden = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'contactForm'
        self.helper.form_class = 'contact-form'
        self.helper.form_method = 'POST'
        self.helper.label_class = 'bold-label'
        self.fields['hidden'].label = False

        self.helper.add_input(Submit('submit', 'Submit'))

        self.helper.layout = Layout(
            Field('name', css_class="contact-name"),
            Field('email', css_class="contact-email"),
            Field('message', css_class="contact-message"),
            Field('hidden', css_class="hidden-field")
        )

class AddGymForm(forms.Form):
    gym_name = forms.CharField(max_length=200)
    gym_location = forms.CharField(max_length=200)
    gym_website = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(AddGymForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'addGym'
        self.helper.form_class = 'add-gym'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('add_gym')
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('gym_name', placeholder="Gym Name", autocomplete="off"),
            Field('gym_location', placeholder="Location", autocomplete="off"),
            Field('gym_website', placeholder="Website/Facebook", autocomplete="off"),
            ButtonHolder(
                HTML('<span id="add-gym-msg"></span>'),
                StrictButton("Submit", type='submit', css_class="btn-outline-primary btn-sm float-right")
            )
        )

class ReviewCreateForm(forms.ModelForm):
    gym = forms.ModelChoiceField(Gym.objects.all(), empty_label="Select Gym")

    class Meta:
        model = Review
        fields = ['gym', 'content', 'session_type', 'start_date', 'end_date', 'rating_training', 
                    'rating_facility', 'rating_location', 'rating_cost', 'rating_overall']
        widgets = {
            'session_type': forms.RadioSelect(attrs={'class': 'custom-control-input'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'rating_training': forms.RadioSelect(attrs={'class': 'custom-control-input'}),
            'rating_facility': forms.RadioSelect(attrs={'class': 'custom-control-input'}),
            'rating_location': forms.RadioSelect(attrs={'class': 'custom-control-input'}),
            'rating_cost': forms.RadioSelect(attrs={'class': 'custom-control-input'}),
            'rating_overall': forms.RadioSelect(attrs={'class': 'custom-control-input'}),
            'content': forms.Textarea(attrs={'cols': '40', 'rows': '15'})
        }
        labels = {
            'session_type': 'Session Type',
            'start_date': 'Training Start Date',
            'end_date': 'Training End Date',
            'rating_training': mark_safe('Rate the Training (Instruction, Trainers, Padwork, Sparring, Clinching, etc.) &#129354;'),
            'rating_facility': mark_safe('Rate the Facilities (Equipment, Hygiene, Onsite Accommodations, etc.) &#127969;'),
            'rating_location': mark_safe('Rate the Location (Nearby Attractions/Housing/Transport/Food, etc.) &#127759;'),
            'rating_cost': mark_safe('Rate the Cost/Value &#128178;'),
            'rating_overall': mark_safe('How would you rate the gym overall? (1 = Bad &#128542;, 3 = Ok &#128528;, 5 = Great! &#128513;)'),
            'content': 'Content'
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if (start_date and not end_date) or (not start_date and end_date):
            raise forms.ValidationError("Please Fill out the other date field")
        elif start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("Invalid End Date")

        return cleaned_data

class ReviewImageForm(forms.ModelForm):
    class Meta:
        model = ReviewImage
        fields = ('image',)
        widgets = {'image': MyImageWidget(attrs={'class':'custom-file-input review-input'})}

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > (5*1024*1024):
                raise forms.ValidationError("Error! Image Exceeds Filesize Limit ( > 5mb )")
            return image
        else:
            raise forms.ValidationError("Couldn't read uploaded image")

ReviewFormSet = forms.inlineformset_factory(Review, ReviewImage, form=ReviewImageForm, extra=1, can_delete=True)