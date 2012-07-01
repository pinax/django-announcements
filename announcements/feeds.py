import datetime

from django.db.models import Q

from atomformat import Feed

from announcements.models import Announcement


class AnnouncementsBase(Feed):
    
    # subclass and set:
    #   feed_id = "..."
    #   feed_title = "..."
    #   feed_links = [
    #     {"rel": "self", "href": "..."},
    #     {"rel": "alternate", "href": "..."},
    #   ]
    #   def item_id
    #   def item_links
    
    def items(self):
        return Announcement.objects.filter(
            publish_start__lte=datetime.datetime.now()
        ).filter(
            Q(publish_end__isnull=True)|Q(publish_end__gt=datetime.datetime.now())
        ).filter(
            site_wide=True
        ).exclude(
            members_only=True
        ).order_by("-creation_date")[:10]
    
    def item_title(self, item):
        return item.title
    
    def item_content(self, item):
        return item.content
    
    def item_authors(self, item):
        return [{"name": str(item.creator)}]
    
    def item_updated(self, item):
        return item.creation_date


