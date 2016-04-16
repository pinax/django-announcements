# Signals

## pinax.announcements.signals.announcement_created

This signal is sent immediately after an announcement is created.
It provides a single `kwarg` of `announcement`, the created `Announcement` instance.
Sender is the newly created Announcement instance.

## pinax.announcements.signals.announcement_updated

This signal is sent immediately after an announcement is updated.
It provides a single `kwarg` of `announcement`, the updated `Announcement` instance.
Sender is the newly updated Announcement instance.

## pinax.announcements.signals.announcement_deleted

This signal is sent immediately after an announcement is deleted.
It provides a single `kwarg` of `announcement`, the deleted `Announcement` instance.
Sender is `None`.
