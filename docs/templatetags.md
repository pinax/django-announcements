# Template Tags

## announcements

Filters announcements by `publish_start` and `publish_end` date range, including
all with no `publish_end` value.
Returns announcements matching `site_wide == True` and `members_only == False`,
and which are not dismissed.

    {% announcements as announcement_list %}
    {% for announcement in announcement_list %}
        <div>
            {{ announcement.title }}<br />
            {{ announcement.content }}
        </div>
    {% endfor %}
