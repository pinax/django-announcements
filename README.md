![](http://pinaxproject.com/pinax-design/patches/pinax-announcements.svg)

# Pinax Announcements

[![](https://img.shields.io/pypi/v/pinax-announcements.svg)](https://pypi.python.org/pypi/pinax-announcements/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-announcements.svg)](https://circleci.com/gh/pinax/pinax-announcements)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-announcements.svg)](https://codecov.io/gh/pinax/pinax-announcements)
[![](https://img.shields.io/github/contributors/pinax/pinax-announcements.svg)](https://github.com/pinax/pinax-announcements/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-announcements.svg)](https://github.com/pinax/pinax-announcements/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-announcements.svg)](https://github.com/pinax/pinax-announcements/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


## Table of Contents

* [About Pinax](#about-pinax)
* [Overview](#overview)
  * [Features](#features)
  * [Supported Django and Python versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Signals](#signals)
  * [Template Tags](#template-tags)
  * [Templates](#templates)
* [Change Log](#change-log)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable
Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.


## pinax-announcements

### Overview

`pinax-announcements` is a well tested, documented, and proven solution
for any site wanting announcements for its users.

#### Features

Announcements have title and content, with options for filtering their display:

* `site_wide` - True or False
* `members_only` - True or False
* `publish_start` - date/time or none
* `publish_end` - date/time or none

`pinax-announcements` has three options for dismissing an announcement:

* `DISMISSAL_NO` - always visible
* `DISMISSAL_SESSION` - dismiss for the session
* `DISMISSAL_PERMANENT` - dismiss forever

#### Supported Django and Python versions

Django \ Python | 2.7 | 3.4 | 3.5 | 3.6
--------------- | --- | --- | --- | ---
1.11 |  *  |  *  |  *  |  *  
2.0  |     |  *  |  *  |  *


## Documentation

### Installation

To install pinax-announcements:

```shell
    $ pip install pinax-announcements
```

Add `pinax.announcements` to your `INSTALLED_APPS` setting:

```python
    INSTALLED_APPS = [
        # other apps
        "pinax.announcements",
    ]
```

Optionally, if you want someone other than staff to manage announcements,
enable this authentication backend:

```python
    AUTHENTICATION_BACKENDS = [
        # other backends
        "pinax.announcements.auth_backends.AnnouncementPermissionsBackend",
    ]
```

then enable permission `"announcements.can_manage"` for these managers.

Lastly add `pinax.announcements.urls` to your project urlpatterns:

```python
    urlpatterns = [
        # other urls
        url(r"^announcements/", include("pinax.announcements.urls", namespace="pinax_announcements")),
    ]
```

### Usage

#### Displaying Announcements

First load the template tags:

```django
    {% load pinax_announcements_tags %}
```

Then fetch announcements with the `announcements` template tag:

```django
    <h3>Announcements</h3>

    {% announcements as announcement_list %}

    {% if announcements_list %}
        <div class="announcements">
            {% for announcement in announcement_list %}
                <div class="announcement">
                    <strong>{{ announcement.title }}</strong><br />
                    {{ announcement.content }}
                </div>
            {% endfor %}
        </div>
    {% endif %}
```

If your announcement content is too large for viewing inline
then show a link to a detail view:

```django
    <a href="{{ announcement.get_absolute_url }}">Read more...</a>
```

See [Template Tags](#template-tags) for detail on pinax-announcements template tags.

#### Dismissing Announcements

Add this markup to show a "Dismiss" link if available:

```django
    {% if announcement.dismiss_url %}
        <form class="form ajax" data-replace-closest=".announcement" action="{{ announcement.dismiss_url }}" method="post">
            {% csrf_token %}
            <button class="btn btn-default">Clear</button>
        </form>
    {% endif %}
```

##### Dismissal with Eldarion AJAX

The anchor markup shown above and the announcement dismissal view both conform
to an `AJAX` response that [eldarion-ajax](https://github.com/eldarion/eldarion-ajax) understands.
Furthermore, the templates that ship with this project will work
seemlessly with `eldarion-ajax`. Include the
eldarion-ajax.min.js Javascript package in your base template:

```django
    {% load staticfiles %}
    <script src="{% static "js/eldarion-ajax.min.js" %}"></script>
```

and include `eldarion-ajax` in your site JavaScript:

```javascript
    require('eldarion-ajax');
```

This of course is optional. You can roll your own JavaScript handling as
the view also returns data in addition to rendered HTML. Furthermore, if
you don't want `ajax` at all the view will handle a regular `POST` and
perform a redirect.

### Signals

#### pinax.announcements.signals.announcement_created

This signal is sent immediately after an announcement is created.
It provides a single `kwarg` of `announcement`, the created `Announcement` instance.
Sender is the newly created Announcement instance.

#### pinax.announcements.signals.announcement_updated

This signal is sent immediately after an announcement is updated.
It provides a single `kwarg` of `announcement`, the updated `Announcement` instance.
Sender is the newly updated Announcement instance.

#### pinax.announcements.signals.announcement_deleted

This signal is sent immediately after an announcement is deleted.
It provides a single `kwarg` of `announcement`, the deleted `Announcement` instance.
Sender is `None`.

### Template Tags

#### announcements

Filters announcements by `publish_start` and `publish_end` date range, including
all with no `publish_end` value.
Returns announcements matching `site_wide == True` and `members_only == False`,
and which are not dismissed.

```django
    {% announcements as announcement_list %}
    {% for announcement in announcement_list %}
        <div>
            {{ announcement.title }}<br />
            {{ announcement.content }}
        </div>
    {% endfor %}
```


### Templates

Default templates are provided by the `pinax-templates` app in the
[announcements](https://github.com/pinax/pinax-templates/tree/master/pinax/templates/templates/pinax/announcements)
section of that project.

Reference pinax-templates
[installation instructions](https://github.com/pinax/pinax-templates/blob/master/README.md#installation)
to include these templates in your project.

#### Customizing Templates

Override the default `pinax-templates` templates by copying them into your project
subdirectory `pinax/announcements/` on the template path and modifying as needed.

For example if your project doesn't use Bootstrap, copy the desired templates
then remove Bootstrap and Font Awesome class names from your copies.
Remove class references like `class="btn btn-success"` and `class="icon icon-pencil"` as well as
`bootstrap` from the `{% load i18n bootstrap %}` statement.
Since `bootstrap` template tags and filters are no longer loaded, you'll also need to update
`{{ form|bootstrap }}` to `{{ form }}` since the "bootstrap" filter is no longer available.

#### `announcement_confirm_delete.html`

#### `announcement_detail.html`

#### `announcement_form.html`

#### `announcement_list.html`

#### `base.html`


## Change Log

### 3.0.2

* Update pinax-templates version requirement

### 3.0.1

* Replace pinax-theme-bootstrap test dependency with pinax-templates

### 3.0.0

* Bump major version after completing Django 2.0 upgrade, removing <=1.10 support

### 2.1.2

* Remove doc build

### 2.1.1

* Standardize documentation layout
* Drop Django v1.8, v1.10 support

### 2.1

* Add Django 2.0 compatibility testing
* Drop Django 1.9 and Python 3.3 support
* Move documentation into README
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description

### 2.0.4

* Fixed dismiss documentation

### 2.0.3

* Convert to Django class-based generic views
* Add URL namespace "pinax_announcements"
* Add tests, including signal handler checking
* Drop support for Django < 1.8
* Improve documentation

### 1.2.0

* Rename to pinax.announcements
* Drop support for django < 1.5
* Rewrite docs for readthedocs with markdown (template based on pinax-blog)
* Update test config (travis, tox, coveragerc, ...)
* Update .gitignore
* Generate django migrations
* Move templates to pinax/announcements/

### 1.0.1

* fixed included templates to be compatible with Django 1.5

### 1.0

* removed atom feed
* renamed dismiss url
* switched to timezone.now
* marked some choice field strings for translation
* swapped view mixin override in favor of auth backend and permission checking

### 0.2

* added ability to publish for periods of time
* added model to store permanent clearings (see migration below)
* added ability to control how announcements are cleared (no
  clearing, session based, or permanent) (see migration below)
* changed view `announcement_hide` to `dismiss`
* changed url name of `announcement_hide` to `announcement_dismiss`
* changed template tag from fetch_announcements to announcements
* removed send now functionality
* removed notifications
* removed context processor
* removed list view
* removed AnnouncementsManager
* removed current_announcements_for_request

### Migrations

Migration scripts to move prior installations to latest version::

    ALTER TABLE "announcements_announcement" ADD COLUMN "dismissal_type" int DEFAULT 2 NOT NULL;
    ALTER TABLE "announcements_announcement" ADD COLUMN "publish_start" timestamp with time zone NOT NULL;
    ALTER TABLE "announcements_announcement" ADD COLUMN "publish_end" timestamp with time zone;
    ### New Model: announcements.Dismissal
    CREATE TABLE "announcements_dismissal" (
        "id" serial NOT NULL PRIMARY KEY,
        "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
        "announcement_id" integer NOT NULL REFERENCES "announcements_announcement" ("id") DEFERRABLE INITIALLY DEFERRED,
        "dismissed_at" timestamp with time zone NOT NULL
    )
    ;
    CREATE INDEX "announcements_dismissal_user_id" ON "announcements_dismissal" ("user_id");
    CREATE INDEX "announcements_dismissal_announcement_id" ON "announcements_dismissal" ("announcement_id");

### 0.1

* initial release


## Contribute

For an overview on how contributing to Pinax works read this [blog post](http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/)
and watch the included video, or read our [How to Contribute](http://pinaxproject.com/pinax/how_to_contribute/) section.
For concrete contribution ideas, please see our
[Ways to Contribute/What We Need Help With](http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions we recommend you join our [Pinax Slack team](http://slack.pinaxproject.com)
and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course
also valid but we are usually able to help you faster if you ping us in Slack.

We also highly recommend reading our blog post on [Open Source and Self-Care](http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project
has a [code of conduct](http://pinaxproject.com/pinax/code_of_conduct/).
We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject)
and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-2018 James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).
