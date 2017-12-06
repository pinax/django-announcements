from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
from django.test import RequestFactory
from django.urls import reverse
from django.utils import timezone

from test_plus.test import TestCase

from ..compat import mock
from ..models import Announcement, Dismissal
from ..templatetags.pinax_announcements_tags import \
    announcements as announcements_tag
from ..views import (
    AnnouncementCreateView,
    AnnouncementDeleteView,
    AnnouncementDetailView,
    AnnouncementListView,
    AnnouncementUpdateView,
)


class TestModels(TestCase):

    def setUp(self):
        super(TestModels, self).setUp()

        self.user = self.make_user("pinax")
        self.title = "Big Announcement"
        self.content = "You won't believe what happened next!"

    def test_model_methods(self):
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.user,
            site_wide=False
        )
        self.assertEqual(
            announcement.get_absolute_url(),
            reverse("pinax_announcements:announcement_detail", kwargs=dict(pk=announcement.pk))
        )
        self.assertEqual(
            announcement.dismiss_url(),
            reverse("pinax_announcements:announcement_dismiss", kwargs=dict(pk=announcement.pk))
        )

        # Verify no dismissal URL available when dismissal is disallowed.
        announcement.dismissal_type = Announcement.DISMISSAL_NO
        announcement.save()
        self.assertEqual(announcement.dismiss_url(), None)


class TestViews(TestCase):

    def setUp(self):
        super(TestViews, self).setUp()

        # Create a non-permissioned user.
        # This user cannot create, update, or delete announcements.
        self.user = self.make_user("pinax")

        # Create a user with "announcements.can_manage" permission.
        self.staff = self.make_user("staff")
        self.staff.is_staff = True
        self.staff.save()
        self.assertTrue(self.staff.has_perm("announcements.can_manage"))

        self.create_urlname = "pinax_announcements:announcement_create"
        self.list_urlname = "pinax_announcements:announcement_list"
        self.detail_urlname = "pinax_announcements:announcement_detail"
        self.dismiss_urlname = "pinax_announcements:announcement_dismiss"
        self.update_urlname = "pinax_announcements:announcement_update"
        self.delete_urlname = "pinax_announcements:announcement_delete"

        self.title = "Big Announcement"
        self.content = "You won't believe what happened next!"

        self.login_redirect = settings.LOGIN_URL

        self.factory = RequestFactory()

    def assertRedirectsToLogin(self, response, next):
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "{}?next={}".format(self.login_redirect, next)
        )

    def get_session_data(self):
        session = Session.objects.get()
        return session.get_decoded()

    def test_list_without_can_manage(self):
        """
        Ensure Announcement views cannot be seen by user without "can_manage" perm.
        """
        url = reverse(self.create_urlname)
        request = self.factory.get(url)
        request.user = self.user
        response = AnnouncementCreateView.as_view()(request)
        self.assertRedirectsToLogin(response, url)

        url = reverse(self.list_urlname)
        request = self.factory.get(url)
        request.user = self.user
        response = AnnouncementListView.as_view()(request)
        self.assertRedirectsToLogin(response, url)

        url = reverse(self.delete_urlname, kwargs=dict(pk=1))
        request = self.factory.get(url)
        request.user = self.user
        response = AnnouncementDeleteView.as_view()(request, pk=1)
        self.assertRedirectsToLogin(response, url)

        url = reverse(self.update_urlname, kwargs=dict(pk=1))
        request = self.factory.get(url)
        request.user = self.user
        response = AnnouncementUpdateView.as_view()(request, pk=1)
        self.assertRedirectsToLogin(response, url)

    def test_user_create(self):
        """
        Ensure POST does not create announcement.
        """
        post_args = dict(
            title=self.title,
            content=self.content,
            site_wide=True,
            dismissal_type=Announcement.DISMISSAL_SESSION,
            publish_start=timezone.now(),
        )
        url = reverse(self.create_urlname)
        request = self.factory.post(url)
        request.user = self.user
        request.POST = post_args
        response = AnnouncementCreateView.as_view()(request)
        self.assertRedirectsToLogin(response, url)

    def test_staff_create(self):
        """
        Ensure POST creates announcement.
        """
        post_args = dict(
            title=self.title,
            content=self.content,
            site_wide=True,
            dismissal_type=Announcement.DISMISSAL_SESSION,
            publish_start=timezone.now(),
        )
        url = reverse(self.create_urlname)
        request = self.factory.post(url)
        request.user = self.staff
        request.POST = post_args
        with mock.patch("pinax.announcements.signals.announcement_created.send", autospec=True) as mocked_handler:
            response = AnnouncementCreateView.as_view()(request)
            self.assertEqual(response.status_code, 302)
            self.assertEquals(mocked_handler.call_count, 1)
            announcement = Announcement.objects.get(title=self.title)
            mocked_handler.assert_called_with(sender=announcement, announcement=announcement, request=request)

    def test_user_detail(self):
        """
        Ensure normal user can see announcement detail.
        """
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.staff,
            site_wide=False
        )
        url = reverse(self.detail_urlname, kwargs=dict(pk=announcement.pk))
        request = self.factory.get(url)
        request.user = self.user
        response = AnnouncementDetailView.as_view()(request, pk=announcement.pk)
        self.assertEqual(response.status_code, 200)
        content_object = response.context_data.get("object")
        self.assertEqual(announcement, content_object)

    def test_user_update(self):
        """
        Ensure non-permissioned user cannot update announcement.
        """
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.staff,
            site_wide=False
        )
        new_title = "Bigger Announcement"
        post_args = dict(
            title=new_title,
        )
        url = reverse(self.update_urlname, kwargs=dict(pk=announcement.pk))
        request = self.factory.post(url)
        request.user = self.user
        request.POST = post_args
        response = AnnouncementUpdateView.as_view()(request, pk=announcement.pk)
        self.assertRedirectsToLogin(response, url)

    def test_staff_update(self):
        """
        Ensure POST updates announcement.
        """
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.staff,
            site_wide=False
        )
        new_title = "Bigger Announcement"
        post_args = dict(
            title=new_title,
            content=announcement.content,
            site_wide=announcement.site_wide,
            dismissal_type=announcement.dismissal_type,
            publish_start=announcement.publish_start
        )
        url = reverse(self.update_urlname, kwargs=dict(pk=announcement.pk))
        request = self.factory.post(url)
        request.user = self.staff
        request.POST = post_args
        with mock.patch("pinax.announcements.signals.announcement_updated.send", autospec=True) as mocked_handler:
            response = AnnouncementUpdateView.as_view()(request, pk=announcement.pk)
            self.assertEqual(response.status_code, 302)
            updated_announcement = Announcement.objects.get(pk=announcement.pk)
            self.assertEqual(updated_announcement.title, new_title)
            self.assertEquals(mocked_handler.call_count, 1)
            mocked_handler.assert_called_with(sender=announcement, announcement=announcement, request=request)

    def test_user_dismiss_session(self):
        """
        Ensure non-permissioned user can dismiss a DISMISSAL_SESSION announcement.
        """
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.staff,
            dismissal_type=Announcement.DISMISSAL_SESSION,
            site_wide=False
        )
        with self.login(self.user):
            response = self.post(self.dismiss_urlname, pk=announcement.pk)
            self.response_200(response)
            self.assertFalse(Dismissal.objects.filter(announcement=announcement))
            session = self.get_session_data()
            excluded = session.get("excluded_announcements", False)
            self.assertTrue(excluded)
            self.assertEqual(excluded, [announcement.pk])

    def test_staff_dismiss_no(self):
        """
        Ensure even staff users cannot dismiss a DISMISSAL_NO announcement.
        """
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.staff,
            dismissal_type=Announcement.DISMISSAL_NO,
            site_wide=False
        )
        with self.login(self.staff):
            response = self.post(self.dismiss_urlname, pk=announcement.pk)
            self.assertEqual(response.status_code, 409)
            self.assertFalse(Dismissal.objects.filter(announcement=announcement))
            session = self.get_session_data()
            self.assertFalse(session.get("excluded_announcements", False))

    def test_user_dismiss_permanent(self):
        """
        Ensure authenticated user can dismiss DISMISSAL_PERMANENT announcement.
        """
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.staff,
            dismissal_type=Announcement.DISMISSAL_PERMANENT,
            site_wide=False
        )
        with self.login(self.user):
            response = self.post(self.dismiss_urlname, pk=announcement.pk)
            self.response_200(response)
            self.assertTrue(announcement.dismissals.all())
            session = self.get_session_data()
            self.assertFalse(session.get("excluded_announcements", False))

    def test_ajax_dismiss_session(self):
        """
        Ensure we dismiss Announcement from the session via AJAX.
        """
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.staff,
            dismissal_type=Announcement.DISMISSAL_SESSION,
            site_wide=False
        )
        with self.login(self.user):
            self.post(
                self.dismiss_urlname,
                pk=announcement.pk,
                extra=dict(HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            )
            self.response_200()
            self.assertFalse(Dismissal.objects.filter(announcement=announcement))
            session = self.get_session_data()
            excluded = session.get("excluded_announcements", False)
            self.assertTrue(excluded)
            self.assertEqual(excluded, [announcement.pk])

    def test_ajax_staff_dismiss_no(self):
        """
        Ensure we don't dismiss Announcement with DISMISSAL_NO via AJAX.
        """
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.staff,
            dismissal_type=Announcement.DISMISSAL_NO,
            site_wide=False
        )
        with self.login(self.staff):
            response = self.post(
                self.dismiss_urlname,
                pk=announcement.pk,
                extra=dict(HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            )
            self.assertEqual(response.status_code, 409)
            self.assertFalse(Dismissal.objects.filter(announcement=announcement))
            session = self.get_session_data()
            self.assertFalse(session.get("excluded_announcements", False))

    def test_ajax_user_dismiss_permanent(self):
        """
        Ensure authenticated user can dismiss DISMISSAL_PERMANENT announcement.
        """
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.staff,
            dismissal_type=Announcement.DISMISSAL_PERMANENT,
            site_wide=False
        )
        with self.login(self.user):
            self.post(
                self.dismiss_urlname,
                pk=announcement.pk,
                extra=dict(HTTP_X_REQUESTED_WITH="XMLHttpRequest")
            )
            self.response_200()
            self.assertTrue(announcement.dismissals.all())
            session = self.get_session_data()
            self.assertFalse(session.get("excluded_announcements", False))

    def test_list(self):
        """
        Ensure Announcement list appears for user with "can_manage" perm.
        """
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.staff,
            site_wide=False
        )
        url = reverse(self.list_urlname)
        request = self.factory.get(url)
        request.user = self.staff
        response = AnnouncementListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        object_list = response.context_data.get("object_list")
        self.assertSequenceEqual(object_list, [announcement])

    def test_user_delete(self):
        """
        Ensure non-permissioned user cannot delete an announcement.
        """
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.staff,
            site_wide=False
        )
        url = reverse(self.delete_urlname, kwargs=dict(pk=announcement.pk))
        request = self.factory.post(url)
        request.user = self.user
        response = AnnouncementDeleteView.as_view()(request, pk=announcement.pk)
        self.assertRedirectsToLogin(response, url)

    def test_staff_delete(self):
        """
        Ensure staff user can delete an announcement.
        """
        announcement = Announcement.objects.create(
            title=self.title,
            content=self.content,
            creator=self.staff,
            site_wide=False
        )
        url = reverse(self.delete_urlname, kwargs=dict(pk=announcement.pk))
        request = self.factory.post(url)
        request.user = self.staff
        with mock.patch("pinax.announcements.signals.announcement_deleted.send", autospec=True) as mocked_handler:
            response = AnnouncementDeleteView.as_view()(request, pk=announcement.pk)
            self.assertEqual(response.status_code, 302)
            self.assertFalse(Announcement.objects.filter(pk=announcement.pk))
            self.assertEquals(mocked_handler.call_count, 1)


class TestTags(TestCase):

    def setUp(self):
        self.user = self.make_user("pinax")
        self.content = "contented"
        self.first = Announcement.objects.create(
            title="first",
            content=self.content,
            creator=self.user,
            site_wide=True
        )

        self.second = Announcement.objects.create(
            title="second",
            content=self.content,
            creator=self.user,
            site_wide=True
        )

    @mock.patch("django.template.Variable")
    def test_announcements(self, Variable):
        """
        Ensure tag returns all announcements.
        """
        parser = mock.Mock()
        token = mock.Mock(methods=["split_contents"])
        token.split_contents.return_value = (
            "announcements",
            "as",
            "announcements_list"
        )
        node = announcements_tag(parser, token)

        request = RequestFactory()
        request.session = {}
        request.user = self.user
        context = dict(request=request)

        node.render(context)
        self.assertSetEqual(set(context["announcements_list"]), set([self.first, self.second]))

        # dismiss one announcement
        self.second.dismissals.create(user=self.user)

        node.render(context)
        self.assertSetEqual(set(context["announcements_list"]), set([self.first]))

    @mock.patch("django.template.Variable")
    def test_anonymous_announcements(self, Variable):
        """
        Ensure tag returns all announcements.
        """
        parser = mock.Mock()
        token = mock.Mock(methods=["split_contents"])
        token.split_contents.return_value = (
            "announcements",
            "as",
            "announcements_list"
        )
        node = announcements_tag(parser, token)

        request = RequestFactory()
        request.session = {}
        request.user = AnonymousUser()
        context = dict(request=request)

        node.render(context)
        self.assertSetEqual(set(context["announcements_list"]), set([self.first, self.second]))
