from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=200)
    team_members = models.ManyToManyField(User, related_name="participating_in_team")
    team_description = models.TextField()
    team_score = models.IntegerField(default=0, editable=False)

    def str_team_members(self):
        return ", ".join(list(self.team_members.values_list("username", flat=True)))

    def __str__(self):
        return self.team_name