import mock

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.test import RequestFactory
from django.utils import timezone

from test_plus.test import TestCase

from ..templatetags.pinax_announcements_tags import announcements as announcements_tag
from ..models import (
    Announcement,
    Dismissal,
)

"""
# Check for signal emitted after test actions!
from ..signals import (
    announcement_created,
    announcement_deleted,
    announcement_updated,
)
"""


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
        # Create user without "can_manage" permission.
        with self.login(self.user):

            response = self.get(self.create_urlname)
            self.assertRedirectsToLogin(response, reverse(self.create_urlname))

            response = self.get(self.list_urlname)
            self.assertRedirectsToLogin(response, reverse(self.list_urlname))

            response = self.get(self.delete_urlname, pk=1)
            self.assertRedirectsToLogin(response, reverse(self.delete_urlname, kwargs=dict(pk=1)))

            response = self.get(self.update_urlname, pk=1)
            self.assertRedirectsToLogin(response, reverse(self.update_urlname, kwargs=dict(pk=1)))

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
        with self.login(self.user):
            response = self.post(self.create_urlname, data=post_args)
            self.assertRedirectsToLogin(response, reverse(self.create_urlname))

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
        with self.login(self.staff):
            response = self.post(self.create_urlname, data=post_args, follow=True)
            self.response_200(response)
            self.assertTrue(Announcement.objects.get(title=self.title))

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
        with self.login(self.user):
            self.get_check_200(self.detail_urlname, pk=announcement.pk)
            content_object = self.get_context("object")
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
        with self.login(self.user):
            response = self.post(self.update_urlname, pk=announcement.pk, data=post_args)
            self.response_302(response)
            self.assertRedirectsToLogin(
                response,
                reverse(self.update_urlname, kwargs=dict(pk=announcement.pk))
            )

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
        with self.login(self.staff):
            response = self.post(
                self.update_urlname,
                pk=announcement.pk,
                data=post_args
            )
            self.response_302(response)
            updated_announcement = Announcement.objects.get(pk=announcement.pk)
            self.assertEqual(updated_announcement.title, new_title)

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
                extra=dict(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
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
                extra=dict(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
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
                extra=dict(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
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
        with self.login(self.staff):
            self.get("pinax_announcements:announcement_list")
            self.response_200()
            self.assertSequenceEqual(self.last_response.context["object_list"], [announcement])

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
        with self.login(self.user):
            response = self.post(self.delete_urlname, pk=announcement.pk)
            self.assertRedirectsToLogin(
                response,
                reverse(self.delete_urlname, kwargs=dict(pk=announcement.pk))
            )

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
        with self.login(self.staff):
            response = self.get(self.delete_urlname, pk=announcement.pk)
            self.response_200(response)
            self.assertTrue(
                'pinax/announcements/announcement_confirm_delete.html' in response.template_name
            )

            response = self.post(self.delete_urlname, pk=announcement.pk, follow=True)
            self.response_200(response)
            self.assertFalse(Announcement.objects.filter(pk=announcement.pk))


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
