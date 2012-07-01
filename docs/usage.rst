.. _usage:

Usage
=====

Displaying announcements is done via a template tag that fetches the
announcements::

    {% load announcements_tags %}
    
    <h3>Announcements</h3>
    
    {% announcements as announcements_list %}
    
    {% if announcements_list %}
        <div class="announcements">
            {% for announcement in announcements_list %}
                <div class="announcement">
                    <strong>{{ announcement.title }}</strong><br />
                    {{ announcement.content }}
                    {% if announcement.dismiss_url %}
                        <a href="{{ announcement.dismiss_url }}" class="dismiss">
                            Clear
                        </a>
                    {% endif %}
                </div>
            {% endfor %}
        </div>
    {% endif %}

If you expect your announcement to be more detail oriented rather than
just a few sentences then it might be better a link in the mark up to
the supplied detail view::

    <a href="{{ announcement.get_absolute_url }}">Read more...</a>


The `announcement.clear_url` is intended to be called via an AJAX POST
and will dismiss the announcement based on it's dismissal properties.