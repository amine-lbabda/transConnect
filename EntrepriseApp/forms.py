from django.contrib.auth.forms import UserCreationForm

from .models import *


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = ("username", "first_name", "email", "telephone")
