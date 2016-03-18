from django.conf.urls import include, url


urlpatterns = [
    url(r"^", include("pinax.announcements.urls", namespace="pinax_announcements")),
]
