# pinax-announcements

Originally named `django-announcements`, the announcements app is now known as `pinax-announcements`.

Some sites need the ability to broadcast an announcement to all of their
users. django-announcements was created precisely for this reason. How you
present the announcement is up to you as the site-developer. There are two
different types of filtering of announcements:

 * site-wide (this can be presented to anonymous users)
 * members only (announcements for only logged in users)

!!! note "Pinax Ecosystem"
    This app was developed as part of the Pinax ecosystem but is just a Django app
    and can be used independently of other Pinax apps.
    
    To learn more about Pinax, see <http://pinaxproject.com/>


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

    url(r"^announcements/", include("pinax.announcements.urls"))


Optionally, if you want someone other than staff users to manage announcements::

    AUTHENTICATION_BACKENDS = [
        ...
        "pinax.announcements.auth_backends.AnnouncementPermissionsBackend",
        ...
    ]

## Dependencies

* `django-appconf>=1.0.1`



