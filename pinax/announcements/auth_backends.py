class AnnouncementPermissionsBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = True

    def authenticate(self, **kwargs):
        # always return a None user
        return None

    def has_perm(self, user, perm, obj=None):
        if perm == "announcements.can_manage":
            if callable(getattr(user, "is_authenticated")):
                # Django v1.8 compatibility
                return user.is_authenticated() and user.is_staff
            else:
                return user.is_authenticated and user.is_staff
