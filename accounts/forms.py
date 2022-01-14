from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.forms.models import ModelForm
from .models import UserPost, UserProfile, Comments


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='',widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='')


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
    date_of_birth = forms.DateField(required=False, label='',widget=forms.DateInput(attrs={'placeholder': 'Date of Birth'}))
    profile_pic = forms.ImageField(
        
        required='',
        widget=forms.FileInput
    )
    cover_pic = forms.ImageField(
        
        required='',
        widget=forms.FileInput
        
    )
    location = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    website = forms.URLField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Website'}))
    bio = widget=forms.TextInput(attrs={'placeholder': 'Bio'})
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


class CommentsForm(forms.ModelForm):
    comments = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Your reply'}
        ),
        required='',
        
    )
    img = forms.ImageField(
        label='',
        required='',
    )

    class Meta:
        model = Comments
        fields = [
            "comments",
            "img"
        ]
