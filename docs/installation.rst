.. _installation:

Installation
============

* To install django-announcements::

    pip install django-announcements

* Add ``'announcements'`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # other apps
        "announcements",
    )

* Finally::

    ...
    url(r"^announcements/", include("announcements.urls")),
    ...
