from django.conf.urls import include, url
from django.http import HttpResponse


def dummy_view(request):
    return HttpResponse(content=b"", status=200)


urlpatterns = [
    url(r"^", include("pinax.announcements.urls", namespace="pinax_announcements")),
    url(r"^dummy_login/$", dummy_view, name="account_login"),
]
