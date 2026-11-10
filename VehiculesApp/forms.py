import typing

from django import forms

from .models import *


class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicules
        fields: typing.ClassVar = "__all__"
