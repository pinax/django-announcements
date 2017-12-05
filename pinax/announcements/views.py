from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from . import signals
from .forms import AnnouncementForm
from .models import Announcement


class AnnouncementDetailView(DetailView):
    template_name = "pinax/announcements/announcement_detail.html"
    model = Announcement
    context_object_name = "announcement"


class AnnouncementDismissView(SingleObjectMixin, View):
    model = Announcement

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.dismissal_type == Announcement.DISMISSAL_SESSION:
            # get list from session and type it to set()
            excluded = set(request.session.get("excluded_announcements", []))
            excluded.add(self.object.pk)
            # force to list to avoid TypeError on set() json serialization
            request.session["excluded_announcements"] = list(excluded)
            status = 200
        elif self.object.dismissal_type == Announcement.DISMISSAL_PERMANENT and \
                request.user.is_authenticated:
            self.object.dismissals.create(user=request.user)
            status = 200
        else:
            status = 409

        if request.is_ajax():
            return JsonResponse({}, status=status)
        else:
            return HttpResponse(content=b"", status=status)


class ProtectedView(View):
    @method_decorator(permission_required("announcements.can_manage"))
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)


class AnnouncementCreateView(ProtectedView, CreateView):
    template_name = "pinax/announcements/announcement_form.html"
    model = Announcement
    form_class = AnnouncementForm
    success_url = reverse_lazy("pinax_announcements:announcement_list")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        signals.announcement_created.send(
            sender=self.object,
            announcement=self.object,
            request=self.request
        )
        return HttpResponseRedirect(self.get_success_url())


class AnnouncementUpdateView(ProtectedView, UpdateView):
    template_name = "pinax/announcements/announcement_form.html"
    model = Announcement
    form_class = AnnouncementForm
    success_url = reverse_lazy("pinax_announcements:announcement_list")

    def form_valid(self, form):
        response = super(AnnouncementUpdateView, self).form_valid(form)
        signals.announcement_updated.send(
            sender=self.object,
            announcement=self.object,
            request=self.request
        )
        return response


class AnnouncementDeleteView(ProtectedView, DeleteView):
    template_name = "pinax/announcements/announcement_confirm_delete.html"
    model = Announcement
    success_url = reverse_lazy("pinax_announcements:announcement_list")

    def delete(self, request, *args, **kwargs):
        response = super(AnnouncementDeleteView, self).delete(request, *args, **kwargs)
#        hookset.announcement_deleted_message(self.request, self.object)
        signals.announcement_deleted.send(
            sender=None,
            announcement=self.object,
            request=self.request
        )
        return response


class AnnouncementListView(ProtectedView, ListView):
    template_name = "pinax/announcements/announcement_list.html"
    model = Announcement
    queryset = Announcement.objects.all().order_by("-creation_date")
    paginate_by = 50
