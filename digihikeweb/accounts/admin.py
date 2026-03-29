from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    exclude = []
    list_display = ["team_name", "str_team_members", "team_score"]