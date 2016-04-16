# Usage

## Displaying Announcements

First load the template tags:

    {% load pinax_announcements_tags %}

Then fetch announcements with the `announcements` template tag:

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

If your announcement content is too large for viewing inline
then show a link to a detail view:

    <a href="{{ announcement.get_absolute_url }}">Read more...</a>

See [Template tags](./templatetags.md) for detail on pinax-announcements template tags.

## Dismissing Announcements

Add this markup to show a "Dismiss" link if available:

                    {% if announcement.dismiss_url %}
                        <a href="{{ announcement.dismiss_url }}" class="btn ajax" data-method="post" data-replace-closest=".announcement">
                            Clear
                        </a>
                    {% endif %}

### Dismissal with Eldarion AJAX

The anchor markup shown above and the announcement dismissal view both conform
to an `AJAX` response that [eldarion-ajax](https://github.com/eldarion/eldarion-ajax) understands.
Furthermore, the templates that ship with this project will work
seemlessly with `eldarion-ajax`. All you have to do is include the
eldarion-ajax.min.js Javascript package in your base template:

    {% load staticfiles %}
    <script src="{% static "js/eldarion-ajax.min.js" %}"></script>

and include `eldarion-ajax` in your site JavaScript:

    require('eldarion-ajax');

This of course is optional. You can roll your own JavaScript handling as
the view also returns data in addition to rendered HTML. Furthermore, if
you don't want `ajax` at all the view will handle a regular `POST` and
perform a redirect.


