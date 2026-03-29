from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


from .forms import TeamAanmeldForm

from .mailer import initialize_team

# Create your views here.
def view_team_aanmelden(request):
    if request.method =="POST":
        form = TeamAanmeldForm(request.POST, request.FILES)
        if form.is_valid():
            initialize_team(form.data)
            return render(request, "aanmelden-gelukt.html")  

    return render(request, "aanmelden.html", context={
        "form": TeamAanmeldForm
    })