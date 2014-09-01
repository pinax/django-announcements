from django.contrib import admin

from announcements.models import Announcement, Dismissal
from announcements.compat import get_user_model


username_search = "user__{0}".format(getattr(get_user_model(), "USERNAME_FIELD", "username"))


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "creation_date", "members_only")
    list_filter = ("members_only",)
    fieldsets = [
        (None, {
            "fields": ["title", "content", "site_wide", "members_only", "publish_start", "publish_end", "dismissal_type"],
        }),
    ]

    def save_model(self, request, obj, form, change):
        if not change:
            # When creating a new announcement, set the creator field.
            obj.creator = request.user
        obj.save()


class DismissalAdmin(admin.ModelAdmin):
    list_display = ("user", "announcement", "dismissed_at")
    search_fields = (username_search, "announcement__title")


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Dismissal, DismissalAdmin)
