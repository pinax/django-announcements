from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import View, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from pinax.announcements import signals
from pinax.announcements.forms import AnnouncementForm
from pinax.announcements.models import Announcement


class AnnouncementDetailView(DetailView):
    template_name = "pinax/announcements/announcement_detail.html"
    model = Announcement
    context_object_name = 'announcement'


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
                request.user.is_authenticated():
            self.object.dismissals.create(user=request.user)
            status = 200
        else:
            status = 409
            if request.is_ajax():
                return JsonResponse({}, status=status)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class ProtectedView(View):
    @method_decorator(permission_required("announcements.can_manage"))
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)


class CreateAnnouncementView(ProtectedView, CreateView):
    template_name = "pinax/announcements/announcement_form.html"
    model = Announcement
    form_class = AnnouncementForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        signals.announcement_created.send(
            sender=self.object,
            announcement=self.object,
            request=self.request
        )
        return super(CreateAnnouncementView, self).form_valid(form)

    def get_success_url(self):
        return reverse("pinax_announcements:announcement_list")


class UpdateAnnouncementView(ProtectedView, UpdateView):
    template_name = "pinax/announcements/announcement_form.html"
    model = Announcement
    form_class = AnnouncementForm

    def form_valid(self, form):
        response = super(UpdateAnnouncementView, self).form_valid(form)
        signals.announcement_updated.send(
            sender=self.object,
            announcement=self.object,
            request=self.request
        )
        return response

    def get_success_url(self):
        return reverse("pinax_announcements:announcement_list")


class DeleteAnnouncementView(ProtectedView, DeleteView):
    template_name = "pinax/announcements/announcement_confirm_delete.html"
    model = Announcement

    def form_valid(self, form):
        response = super(DeleteAnnouncementView, self).form_valid(form)
        signals.announcement_deleted.send(
            sender=self.object,
            announcement=self.object,
            request=self.request
        )
        return response

    def get_success_url(self):
        return reverse("pinax_announcements:announcement_list")


class AnnouncementListView(ProtectedView, ListView):
    template_name = "pinax/announcements/announcement_list.html"
    model = Announcement
    queryset = Announcement.objects.all().order_by("-creation_date")
    paginate_by = 50
