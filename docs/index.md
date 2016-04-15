# pinax-announcements

[Pinax](http://pinaxproject.com/pinax/) is an open source ecosystem
of reusable Django apps, themes, and starter project templates.

As a reusable Django app, `pinax-announcements` provides the ecosystem with
a well tested, documented, and proven solution for any site that
that wants to support announcements for either members only or for all users.

Some sites need the ability to broadcast an announcement to all of their
users. django-announcements was created precisely for this reason. How you
present the announcement is up to you as the site-developer. There are two
different types of filtering of announcements:

 * site-wide (this can be presented to anonymous users)
 * members only (announcements for only logged in users)

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
