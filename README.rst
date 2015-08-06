django-announcements
--------------------

.. image:: http://slack.pinaxproject.com/badge.svg
   :target: http://slack.pinaxproject.com/

.. image:: https://img.shields.io/travis/pinax/django-announcements.svg
    :target: https://travis-ci.org/pinax/django-announcements

.. image:: https://img.shields.io/coveralls/pinax/django-announcements.svg
    :target: https://coveralls.io/r/pinax/django-announcements

.. image:: https://img.shields.io/pypi/dm/django-announcements.svg
    :target:  https://pypi.python.org/pypi/django-announcements/

.. image:: https://img.shields.io/pypi/v/django-announcements.svg
    :target:  https://pypi.python.org/pypi/django-announcements/

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target:  https://pypi.python.org/pypi/django-announcements/


Some sites need the ability to broadcast an announcement to all of their
users. django-announcements was created precisely for this reason. How you
present the announcement is up to you as the site-developer. When working with
announcements that are presented on the website one feature is that they are
only viewed once. A session variable will hold which announcements an user has
viewed and exclude that from their display. announcements supports two
different types of filtering of announcements:

* site-wide (this can be presented to anonymous users)
* non site-wide (these can be used a strictly a mailing if so desired)
* members only (announcements are filtered based on the value of
   ``request.user``)
