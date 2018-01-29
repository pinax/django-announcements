from setuptools import find_packages, setup

VERSION = "3.0.2"
LONG_DESCRIPTION = """
.. image:: http://pinaxproject.com/pinax-design/patches/pinax-announcements.svg
    :target: https://pypi.python.org/pypi/pinax-announcements/

===================
Pinax Announcements
===================

.. image:: https://img.shields.io/pypi/v/pinax-announcements.svg
    :target: https://pypi.python.org/pypi/pinax-announcements/

\ 

.. image:: https://img.shields.io/circleci/project/github/pinax/pinax-announcements.svg
    :target: https://circleci.com/gh/pinax/pinax-announcements
.. image:: https://img.shields.io/codecov/c/github/pinax/pinax-announcements.svg
    :target: https://codecov.io/gh/pinax/pinax-announcements
.. image:: https://img.shields.io/github/contributors/pinax/pinax-announcements.svg
    :target: https://github.com/pinax/pinax-announcements/graphs/contributors
.. image:: https://img.shields.io/github/issues-pr/pinax/pinax-announcements.svg
    :target: https://github.com/pinax/pinax-announcements/pulls
.. image:: https://img.shields.io/github/issues-pr-closed/pinax/pinax-announcements.svg
    :target: https://github.com/pinax/pinax-announcements/pulls?q=is%3Apr+is%3Aclosed

\ 

.. image:: http://slack.pinaxproject.com/badge.svg
    :target: http://slack.pinaxproject.com/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT/

\ 

``pinax-announcements`` is a well tested, documented, and proven solution
for any site wanting announcements for it's users.

Announcements have title and content, with options for filtering their display:

* ``site_wide`` - True or False
* ``members_only`` - True or False
* ``publish_start`` - date/time or none
* ``publish_end`` - date/time or none

``pinax-announcements`` has three options for dismissing an announcement:

* ``DISMISSAL_NO`` - always visible
* ``DISMISSAL_SESSION`` - dismiss for the session
* ``DISMISSAL_PERMANENT`` - dismiss forever

Supported Django and Python Versions
------------------------------------

+-----------------+-----+-----+-----+-----+
| Django / Python | 2.7 | 3.4 | 3.5 | 3.6 |
+=================+=====+=====+=====+=====+
|  1.11           |  *  |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
|  2.0            |     |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
"""

setup(
    author="Pinax Team",
    author_email="team@pinaxproject.com",
    description="a Django announcements app",
    name="pinax-announcements",
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    url="http://github.com/pinax/pinax-announcements/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "announcements": []
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "django>=1.11",
    ],
    tests_require=[
        "django-test-plus>=1.0.22",
        "pinax-templates>=1.0.4",
        "mock>=2.0.0",
    ],
    test_suite="runtests.runtests",
    zip_safe=False
)
