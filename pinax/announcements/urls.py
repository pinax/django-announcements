from django.conf.urls import url

from pinax.announcements import views

urlpatterns = [
    url(r"^$", views.AnnouncementListView.as_view(), name="announcements_list"),
    url(r"^announcement/create/$", views.CreateAnnouncementView.as_view(), name="announcements_create"),
    url(r"^announcement/(?P<pk>\d+)/$", views.detail, name="announcements_detail"),
    url(r"^announcement/(?P<pk>\d+)/hide/$", views.dismiss, name="announcements_dismiss"),
    url(r"^announcement/(?P<pk>\d+)/update/$", views.UpdateAnnouncementView.as_view(), name="announcements_update"),
    url(r"^announcement/(?P<pk>\d+)/delete/$", views.DeleteAnnouncementView.as_view(), name="announcements_delete"),
]
