from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User

from crazy88.models import Team

import string

def initialize_team(data):
    new_user1, pwd1 = create_user(data["name1"], data["email1"])
    new_user2, pwd2 = create_user(data["name2"], data["email2"])

    personalized_initial_mail(new_user1.username, new_user1.email, pwd1)
    personalized_initial_mail(new_user2.username, new_user2.email, pwd2)

    new_team = Team.objects.create(
        team_name = data["team_name"],
        team_description = ""
    )

    new_team.team_members.set([new_user1, new_user2])

def create_user(username, email):
    pwd = BaseUserManager.make_random_password("",6, string.ascii_uppercase)
    new_user = User.objects.create_user(
        username = username,
        email= email,
        password = pwd,
    )

    return new_user, pwd

def personalized_initial_mail(username, email, pwd):    
    send_mail(
        "Inloggegevens van {}".format(username),
        """
        Hoi {} leuk dat je je hebt aangemeld, hierbij je inloggegevens:
        Gebrukkersnaam: {}
        wachtwoord: {}
        """.format(username, username, pwd),
        "hielke@ba-ow.nl",
        [email],
        fail_silently=False,
    )
    
    print("mail send")