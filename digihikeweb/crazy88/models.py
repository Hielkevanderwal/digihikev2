import os
import shutil
import subprocess
import tempfile
import threading

from django.conf import settings
from django.db import models
from django.core.validators import FileExtensionValidator

from accounts.models import Team

VIDEO_EXTENSIONS = {
    'mp4', 'mov', 'mkv', 'webm', 'avi', 'flv', 'mpeg', 'mpg', '3gp', 'ogv', 'ts', 'm4v'
}
IMAGE_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'tiff', 'tif', 'svg', 'heic'
}
ALLOWED_EXTENSIONS = sorted(VIDEO_EXTENSIONS | IMAGE_EXTENSIONS)

# Create your models here.

class MediaType(models.TextChoices):
    VIDEO = 'video', 'Video'
    PHOTO = 'foto', 'Photo'
    TEXT = 'tekst', 'Text'
    BOTH = 'foto/video', 'Foto/Video'

class MissionGroup(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def get_nr_missions(self):
        return self.missions.count()
    
    def __str__(self):
        return self.name

class Mission(models.Model):
    title = models.CharField(max_length=120)
    points = models.IntegerField(default=5)
    description = models.TextField()
    capture_type = models.CharField(
        max_length=10, 
        choices=MediaType.choices, 
        default=MediaType.BOTH
    )

    group = models.ForeignKey(MissionGroup, on_delete=models.CASCADE, related_name="missions")

    def __str__(self):
        return self.title
    
    def teams_completed(self):
        return Team.objects.filter(submission__mission=self, submission__validated=True).distinct()
    

class Submission(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)

    bonuspoints = models.IntegerField(default=0)

    upload_date = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    feedback = models.TextField(blank=True)

    media = models.FileField(
        upload_to='uploads', 
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)]
    )
    
    validated = models.BooleanField(null=True, blank=True)

    def is_vid(self):
        name, extension = os.path.splitext(self.media.name)
        return extension.lower().lstrip('.') in VIDEO_EXTENSIONS
    
    def save(self, *args, **kwargs):
        skip_compression = kwargs.pop('_skip_video_compression', False)
        super().save(*args, **kwargs)
        if self.is_vid() and not skip_compression:
            self._compress_video_async()
        if self.validated:
            self.recalculate_score(self.team)

    def _compress_video_async(self):
        thread = threading.Thread(target=self._compress_video_worker, args=(self.pk,), daemon=True)
        thread.start()

    @staticmethod
    def _compress_video_worker(pk):
        try:
            instance = Submission.objects.get(pk=pk)
        except Submission.DoesNotExist:
            return

        if not instance.is_vid():
            return

        input_path = instance.media.path
        output_path = None
        file_root, ext = os.path.splitext(input_path)
        target_path = input_path if ext.lower() == '.mp4' else f"{file_root}.mp4"

        try:
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
                output_path = temp_file.name

            subprocess.run(
                [
                    'ffmpeg',
                    '-y',
                    '-i', input_path,
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-crf', '28',
                    '-vf', "scale='min(iw,1280)':-2",
                    '-c:a', 'aac',
                    '-b:a', '128k',
                    '-movflags', '+faststart',
                    output_path,
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            shutil.move(output_path, target_path)
            if target_path != input_path:
                if os.path.exists(input_path):
                    os.remove(input_path)
                new_name = os.path.relpath(target_path, settings.MEDIA_ROOT).replace(os.sep, '/')
                Submission.objects.filter(pk=pk).update(media=new_name)
        except (FileNotFoundError, subprocess.CalledProcessError):
            if output_path and os.path.exists(output_path):
                os.remove(output_path)
        finally:
            if output_path and os.path.exists(output_path):
                os.remove(output_path)

    def recalculate_score(self,team):
        ms = Submission.objects.filter(validated=True, team=team)
        score = sum([m.mission.points + m.bonuspoints for m in ms])
        team.team_score = score
        team.save()

        print(score)