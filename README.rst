Django Announcements
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
    

Pinax
------

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. 
This collection can be found at http://pinaxproject.com.

This app was developed as part of the Pinax ecosystem but is just a Django app and can be used independently of other Pinax apps.


django-announcements
---------------------

``django-announcements`` is a site-wide announcement reusable app for Django.

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
  
  
Documentation
----------------

The django-announcements documentation can be found at https://django-announcements.readthedocs.org/en/latest/. The Pinax documentation is available at http://pinaxproject.com/pinax/. If you would like to help us improve our documentation or write more documentation, please join our Pinax Project Slack channel and let us know!


Code of Conduct
-----------------

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a code of conduct, which can be found here  http://pinaxproject.com/pinax/code_of_conduct/.


Pinax Project Blog and Twitter
-------------------------------

For updates and news regarding the Pinax Project, please follow us on Twitter at @pinaxproject and check out our blog http://blog.pinaxproject.com.
