from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.forms.models import ModelForm
from .models import UserPost, UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class CreateRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]



class EditRegister(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
        ]
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "date_of_birth",
            "profile_pic",
            "cover_pic",
            "location",
            "website",
            "bio",
        ]

class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = [
            "tweet_post",
            "img"
        ]