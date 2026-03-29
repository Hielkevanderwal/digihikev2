from django.contrib import admin

from .models import Submission, Mission, MissionGroup

# Register your models here.

admin.site.register(Mission)
admin.site.register(MissionGroup)


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