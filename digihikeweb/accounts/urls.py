from django.urls import path
from .views import *

urlpatterns = [
    path("team_aanmelden", view_team_aanmelden, name="team_aanmelden"),
]