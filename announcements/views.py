from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from announcements.forms import AnnouncementForm
from announcements.mixins import ProtectedMixin
from announcements.models import Announcement
from announcements.signals import announcement_created, announcement_updated, announcement_deleted


def dismiss(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if announcement.dismissal_type == Announcement.DISMISSAL_SESSION:
        excluded = request.session.get("excluded_announcements", set())
        excluded.add(announcement.pk)
        request.session["excluded_announcements"] = excluded
        status = 200
    elif announcement.dismissal_type == Announcement.DISMISSAL_PERMANENT and request.user.is_authenticated():
        announcement.dismissals.create(user=request.user)
        status = 200
    else:
        status = 409
    
    return HttpResponse(status=status)


def detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return TemplateResponse(request, "announcements/detail.html", {
        "announcement": announcement
    })


class CreateAnnouncementView(CreateView, ProtectedMixin):
    
    model = Announcement
    form_class = AnnouncementForm
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        
        announcement_created.send(
            sender=self.object,
            announcement=self.object,
            request=self.request
        )
        return super(CreateAnnouncementView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse("announcements_list")


class UpdateAnnouncementView(UpdateView, ProtectedMixin):
    
    model = Announcement
    form_class = AnnouncementForm
    
    def form_valid(self, form):
        response = super(UpdateAnnouncementView, self).form_valid(form)
        announcement_updated.send(
            sender=self.object,
            announcement=self.object,
            request=self.request
        )
        return response
    
    def get_success_url(self):
        return reverse("announcements_list")


class DeleteAnnouncementView(DeleteView, ProtectedMixin):
    
    model = Announcement
    
    def form_valid(self, form):
        response = super(DeleteAnnouncementView, self).form_valid(form)
        announcement_deleted.send(
            sender=self.object,
            announcement=self.object,
            request=self.request
        )
        return response
    
    def get_success_url(self):
        return reverse("announcements_list")


class AnnouncementListView(ListView, ProtectedMixin):
    
    model = Announcement
    queryset = Announcement.objects.all().order_by("-creation_date")
    paginate_by = 50
