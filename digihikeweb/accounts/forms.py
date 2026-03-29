from django import forms
from django.contrib.auth.models import User

class TeamAanmeldForm(forms.Form):
    team_name = forms.CharField(max_length=200)

    name1 = forms.CharField(max_length=100)
    email1 = forms.EmailField()

    name2 = forms.CharField(max_length=100)
    email2 = forms.EmailField()

    voorwaarden_geaccepteerd = forms.BooleanField(required=False)
