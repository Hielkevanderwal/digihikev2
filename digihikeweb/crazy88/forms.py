from django.forms import ModelForm

from .models import Submission

class MissionUploadForm(ModelForm):
    class Meta:
        model = Submission
        fields = ["media","description"]
