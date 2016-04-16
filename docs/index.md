# pinax-announcements

## Quickstart

Install the development version:

    pip install pinax-announcements

Add `pinax.announcements` to your `INSTALLED_APPS` setting:

    INSTALLED_APPS = (
        # ...
        "pinax.announcements",
        # ...
    )

Add entry to your `urls.py`:

    url(r"^announcements/", include("pinax.announcements.urls", namespace="pinax_announcements")),


Optionally, if you want someone other than staff users to manage announcements::

    AUTHENTICATION_BACKENDS = [
        ...
        "pinax.announcements.auth_backends.AnnouncementPermissionsBackend",
        ...
    ]

See also [Usage](./usage.md) for implementation details and [Changelog](./changelog.md) for a list of changes.
