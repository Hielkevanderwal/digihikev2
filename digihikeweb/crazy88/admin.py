from django.contrib import admin

from .models import Submission, Mission, MissionGroup

# Register your models here.

@admin.register(MissionGroup)
class MissionGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_filter = ("active",)z

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("title", "points", "capture_type", "group")
    list_filter = ("capture_type", "group")
    search_fields = ("title", "description")

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("team", "mission", "upload_date", "validated")
    list_filter = ("validated", "upload_date")
    search_fields = ("team__team_name", "mission__title")
    actions = ["set_validated_true", "set_validated_false"]

    @admin.action(description="Mark selected submissions as validated")
    def set_validated_true(self, request, queryset):
        updated = queryset.update(validated=True)
        self.message_user(request, f"{updated} submission(s) marked validated.")

    @admin.action(description="Mark selected submissions as not validated")
    def set_validated_false(self, request, queryset):
        updated = queryset.update(validated=False)
        self.message_user(request, f"{updated} submission(s) marked not validated.")