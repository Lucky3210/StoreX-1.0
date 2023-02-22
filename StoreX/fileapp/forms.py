from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class MyUserCreationForm(UserCreationForm):
    firstname = forms.CharField()
    lastname = forms.CharField()
    # phone = forms.

    class Meta:
        model = User
        # when the user is registering what fields do we want to render out, that's what this field is implementing
        fields = ['firstname', 'lastname', 'phone', 'email', 'password1', 'password2']