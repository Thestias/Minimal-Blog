from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from markdownx.fields import MarkdownxFormField


class CustomUserCreation(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MarkdownX(forms.Form):
    markdown = MarkdownxFormField()
