from django.conf.urls import url

from pinax.announcements import views

urlpatterns = [
    url(r"^$", views.AnnouncementListView.as_view(),
        name="announcement_list"),
    url(r"^create/$", views.CreateAnnouncementView.as_view(),
        name="announcement_create"),
    url(r"^(?P<pk>\d+)/$", views.AnnouncementDetailView.as_view(),
        name="announcement_detail"),
    url(r"^(?P<pk>\d+)/hide/$", views.AnnouncementDismissView.as_view(),
        name="announcement_dismiss"),
    url(r"^(?P<pk>\d+)/update/$", views.UpdateAnnouncementView.as_view(),
        name="announcement_update"),
    url(r"^(?P<pk>\d+)/delete/$", views.DeleteAnnouncementView.as_view(),
        name="announcement_delete"),
]
