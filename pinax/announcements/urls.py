from django.conf.urls import url

from .views import (
    AnnouncementCreateView,
    AnnouncementDeleteView,
    AnnouncementDetailView,
    AnnouncementDismissView,
    AnnouncementListView,
    AnnouncementUpdateView,
)

app_name = "pinax_announcements"

urlpatterns = [
    url(r"^$", AnnouncementListView.as_view(), name="announcement_list"),
    url(r"^create/$", AnnouncementCreateView.as_view(), name="announcement_create"),
    url(r"^(?P<pk>\d+)/$", AnnouncementDetailView.as_view(), name="announcement_detail"),
    url(r"^(?P<pk>\d+)/hide/$", AnnouncementDismissView.as_view(), name="announcement_dismiss"),
    url(r"^(?P<pk>\d+)/update/$", AnnouncementUpdateView.as_view(), name="announcement_update"),
    url(r"^(?P<pk>\d+)/delete/$", AnnouncementDeleteView.as_view(), name="announcement_delete"),
]
