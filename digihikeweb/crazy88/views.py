from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


from accounts.models import Team
from .models import Submission, MissionGroup, Mission
from .forms import MissionUploadForm

from random import choice

# Create your views here.
@login_required
def crazy88_view_home(request):
    active_mission_groups = MissionGroup.objects.filter(active = True)
    
    return render(request, "crazy88/overview.html", context={
        "teams": Team.objects.all().order_by('-team_score'),
        "active_mission_groups": active_mission_groups
    })

@login_required
def crazy88_view_list(request, mission_group_name):
    mission_group = get_object_or_404(MissionGroup, name = mission_group_name)

    return render(request, "crazy88/list.html", context={
        "mission_group": mission_group,
        "missions": mission_group.missions.all()
    })

@login_required
def view_detailed_task(request, mission_group_name, mission_title):

    if request.method == "POST":
        form = MissionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_sub = form.save(commit=False)
            new_sub.team = Team.objects.filter(team_members__in=[request.user]).first()
            new_sub.mission = Mission.objects.filter(title = mission_title).first() 

            new_sub.save()

            return HttpResponseRedirect('')

    mission_group = get_object_or_404(MissionGroup, name = mission_group_name)
    mission = mission_group.missions.filter(title = mission_title).first()


    submissions = Submission.objects.filter(mission = mission).order_by("-upload_date")
    team = Team.objects.filter(team_members__in=[request.user]).first()

    # Prevent uploads when there is already an approved or pending submission.
    can_upload = bool(team) and not submissions.filter(team=team).exclude(validated=False).exists()

    return render(request, "crazy88/detailed.html", context={
        "mission_group": mission_group,
        "mission": mission,
        "missione_xecutions": submissions,
        "show_upload": can_upload,
        "upload_form": MissionUploadForm,
    })

