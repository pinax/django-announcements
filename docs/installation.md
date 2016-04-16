# Installation

To install pinax-announcements:

    pip install pinax-announcements

Add `pinax.announcements` to your `INSTALLED_APPS` setting:

    INSTALLED_APPS = (
        ...
        "pinax.announcements",
        ...
    )

Optionally, if you want someone other than staff to manage announcements,
enable this authentication backend:

    AUTHENTICATION_BACKENDS = [
        ...
        "pinax.announcements.auth_backends.AnnouncementPermissionsBackend",
        ...
    ]

then enable permission `"announcements.can_manage"` for these managers.

Lastly add `pinax.announcements.urls` to your project urlpatterns.py:

    urlpatterns = [
        ...
        url(r"^announcements/", include("pinax.announcements.urls", namespace="pinax_announcements")),
        ...
    ]

See [Usage](./usage.md) for details about integrating pinax-announcements with your project.
