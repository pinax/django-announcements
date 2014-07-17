django-announcements
--------------------

.. image:: https://img.shields.io/travis/pinax/pinax-wiki.svg
    :target: https://travis-ci.org/pinax/pinax-wiki

.. image:: https://img.shields.io/coveralls/pinax/pinax-wiki.svg
    :target: https://coveralls.io/r/pinax/pinax-wiki

.. image:: https://img.shields.io/pypi/dm/pinax-wiki.svg
    :target:  https://pypi.python.org/pypi/pinax-wiki/

.. image:: https://img.shields.io/pypi/v/pinax-wiki.svg
    :target:  https://pypi.python.org/pypi/pinax-wiki/

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target:  https://pypi.python.org/pypi/pinax-wiki/


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
