Pinax Announcements
--------------------

.. image:: http://slack.pinaxproject.com/badge.svg
   :target: http://slack.pinaxproject.com/

.. image:: https://img.shields.io/travis/pinax/pinax-announcements.svg
    :target: https://travis-ci.org/pinax/pinax-announcements

.. image:: https://img.shields.io/coveralls/pinax/pinax-announcements.svg
    :target: https://coveralls.io/r/pinax/pinax-announcements

.. image:: https://img.shields.io/pypi/dm/pinax-announcements.svg
    :target:  https://pypi.python.org/pypi/pinax-announcements/

.. image:: https://img.shields.io/pypi/v/pinax-announcements.svg
    :target:  https://pypi.python.org/pypi/pinax-announcements/

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target:  https://pypi.python.org/pypi/pinax-announcements/
    

Pinax
------

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. 
This collection can be found at http://pinaxproject.com.

This app was developed as part of the Pinax ecosystem but is just a Django app and can be used independently of other Pinax apps.


pinax-announcements
---------------------

``pinax-announcements`` is a site-wide announcement reusable app for Django.

Some sites need the ability to broadcast an announcement to all of their
users. pinax-announcements was created precisely for this reason. How you
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

The ``pinax-announcements`` documentation can be found at https://django-announcements.readthedocs.org/en/latest/. The Pinax documentation is available at http://pinaxproject.com/pinax/. If you would like to help us improve our documentation or write more documentation, please join our Pinax Project Slack team and let us know!


Contribute
----------------

See this blog post http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/ including a video, or our How to Contribute (http://pinaxproject.com/pinax/how_to_contribute/) section for an overview on how contributing to Pinax works. For concrete contribution ideas, please see our Ways to Contribute/What We Need Help With (http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions we recommend you join our Pinax Slack team (http://slack.pinaxproject.com) and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course also valid but we are usually able to help you faster if you ping us in Slack.

We also highly recommend reading our Open Source and Self-Care blog post (http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/).  


Code of Conduct
-----------------

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a code of conduct, which can be found here  http://pinaxproject.com/pinax/code_of_conduct/. 
We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.



Pinax Project Blog and Twitter
-------------------------------

For updates and news regarding the Pinax Project, please follow us on Twitter at @pinaxproject and check out our blog http://blog.pinaxproject.com.
