from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django import forms
from django import forms
from django.forms import ModelForm, ValidationError, FileField


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = forms.TextInput(attrs={'class': 'form-control', 'palceholder': '', 'id': 'hello'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'palceholder': '', 'id': 'hi'}))



MAX_UPLOAD_SIZE = 2500000

class ProfileForm(ModelForm):
    # avatar = FileField(required=False)

    class Meta:
        model = Profile
        fields = ["bio", "avatar"]

    def clean_avatar(self):
        picture = self.cleaned_data['avatar']

        if not picture:
            return picture
        if not picture or not hasattr(picture, 'content_type'):
            raise ValidationError('You must upload a picture')
        if picture.content_type and not picture.content_type.startswith('image'):
            raise ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture

class CASignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.save()
        return user
