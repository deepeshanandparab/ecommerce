from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_image','user_bio','contact_number','facebook_link','instagram_link','twitter_link']