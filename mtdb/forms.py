from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Field, HTML
from users.forms import MyImageWidget
from .models import Review, Gym, ReviewImage

class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'contactForm'
        self.helper.form_class = 'contact-form'
        self.helper.form_method = 'POST'

        self.helper.add_input(Submit('submit', 'Submit'))

        self.helper.layout = Layout(
            Field('name', css_class="contact-name"),
            Field('email', css_class="contact-email"),
            Field('message', css_class="contact-message")
        )

class ReviewCreateForm(forms.ModelForm):
    gym = forms.ModelChoiceField(Gym.objects.all(), empty_label="Select Gym")

    class Meta:
        model = Review
        fields = ['gym', 'content', 'start_date', 'end_date', 'rating_training', 
                    'rating_facility', 'rating_location', 'rating_cost', 'rating_overall']
        widgets = {
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
            'start_date': 'Training Start Date',
            'end_date': 'Training End Date',
            'rating_training': 'Rate the Training (Instruction, Trainers, Padwork, Sparring, Clinching, etc.)',
            'rating_facility': 'Rate the Facilities (Equipment, Hygiene, Onsite Accommodations, etc.)',
            'rating_location': 'Rate the Location/Surrounding Area (Nearby Attractions/Housing/Transport/Food, etc.)',
            'rating_cost': 'Rate the Cost/Value',
            'rating_overall': 'Overall Rating',
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