from django.contrib.sessions.models import Session
from django.template import Template

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
from .test import TestCase


class TestCaseMixin(object):

    def assert_renders(self, tmpl, context, value):
        tmpl = Template(tmpl)
        self.assertEqual(tmpl.render(context).strip(), value)


class BaseTest(TestCase, TestCaseMixin):
    def setUp(self):
        self.staff = self.make_user("staff")
        # Make this user "staff" for "can_manage" permission.
        self.staff.is_staff = True
        self.staff.save()
        self.assertTrue(self.staff.has_perm("announcements.can_manage"))


class TestViews(BaseTest):

    def test_list_without_can_manage(self):
        """
        Ensure Announcement list DOES NOT appear for user without "can_manage" perm.
        """
        # Create user without "can_manage" permission.
        user = self.make_user("user")
        with self.login(user):

            self.get("pinax_announcements:announcement_create")
            self.response_302()

            self.get("pinax_announcements:announcement_list")
            self.response_302()

            self.get("pinax_announcements:announcement_delete", pk=1)
            self.response_302()

            self.get("pinax_announcements:announcement_update", pk=1)
            self.response_302()

    def test_create(self):
        """
        Ensure Announcement is created properly.
        """
        title = "More Election Results"
        post_args = {
            "title": title,
            "content": "more results",
            "site_wide": False,
            "members_only": False,
            "dismissal_type": 1,
            "publish_start": "2016-03-11",
            "publish_end": "",
        }
        with self.login(self.staff):
            response = self.post(
                "pinax_announcements:announcement_create",
                data=post_args,
                follow=True
            )
            self.response_200(response)
            self.assertTrue(Announcement.objects.filter(title=title))

    def test_detail(self):
        """
        Ensure view context contains the expected Announcement.
        """
        announcement = Announcement.objects.create(
            title="Election Results",
            content="some results",
            creator=self.staff
        )
        announcement.save()

        # User without "can_manage" perm is able to view detail.
        user = self.make_user("user")
        with self.login(user):
            self.get("pinax_announcements:announcement_detail", pk=announcement.pk)
            self.response_200()
            self.assertContext("object", announcement)

    def test_update(self):
        """
        Ensure Announcement is updated.
        """
        announcement = Announcement.objects.create(
            title="Election Results",
            content="some results",
            creator=self.staff
        )
        announcement.save()

        new_title = "2016 Election Results"
        post_args = {
            "title": new_title,
            "content": "more results",
            "site_wide": False,
            "members_only": False,
            "dismissal_type": 1,
            "publish_start": "2016-03-11",
            "publish_end": "",
        }
        with self.login(self.staff):
            response = self.post(
                "pinax_announcements:announcement_update",
                pk=announcement.pk,
                data=post_args,
                follow=True
            )
            self.response_200(response)
            self.assertTrue(Announcement.objects.filter(title=new_title))

    def get_session_data(self):
        session = Session.objects.get()
        return session.get_decoded()

    def test_dismiss_no(self):
        """
        Ensure we don't dismiss Announcement with DISMISSAL_NO.
        """
        announcement = Announcement.objects.create(
            title="Election Results",
            content="some results",
            creator=self.staff,
            dismissal_type=Announcement.DISMISSAL_NO
        )
        announcement.save()

        # Create user without "can_manage" permission.
        user = self.make_user("user")
        with self.login(user):
            self.post("pinax_announcements:announcement_dismiss", pk=announcement.pk)
            self.response_302()
            self.assertFalse(Dismissal.objects.filter(announcement=announcement))
            session = self.get_session_data()
            self.assertFalse(session.get("excluded_announcements", False))

    def test_dismiss_session(self):
        """
        Ensure we dismiss Announcement from the session.
        """
        announcement = Announcement.objects.create(
            title="Election Results",
            content="some results",
            creator=self.staff,
            dismissal_type=Announcement.DISMISSAL_SESSION
        )
        announcement.save()

        # Create user without "can_manage" permission.
        user = self.make_user("user")
        with self.login(user):
            self.post("pinax_announcements:announcement_dismiss", pk=announcement.pk)
            self.response_302()
            self.assertFalse(Dismissal.objects.filter(announcement=announcement))
            session = self.get_session_data()
            excluded = session.get("excluded_announcements", False)
            self.assertTrue(excluded)
            self.assertEqual(excluded, [announcement.pk])

    def test_dismiss_permanent(self):
        """
        Ensure we dismiss Announcement permanently.
        """
        announcement = Announcement.objects.create(
            title="Election Results",
            content="some results",
            creator=self.staff,
            dismissal_type=Announcement.DISMISSAL_PERMANENT
        )
        announcement.save()

        # Create user without "can_manage" permission.
        user = self.make_user("user")
        with self.login(user):
            self.post("pinax_announcements:announcement_dismiss", pk=announcement.pk)
            self.response_302()
            self.assertTrue(Dismissal.objects.filter(announcement=announcement))
            session = self.get_session_data()
            self.assertFalse(session.get("excluded_announcements", False))

    def test_ajax_dismiss_no(self):
        """
        Ensure we don't dismiss Announcement with DISMISSAL_NO via AJAX.
        """
        announcement = Announcement.objects.create(
            title="Election Results",
            content="some results",
            creator=self.staff,
            dismissal_type=Announcement.DISMISSAL_NO
        )
        announcement.save()

        # Create user without "can_manage" permission.
        user = self.make_user("user")
        with self.login(user):
            response = self.post(
                "pinax_announcements:announcement_dismiss",
                pk=announcement.pk,
                extra=dict(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            )
            self.assertEqual(response.status_code, 409)
            self.assertFalse(Dismissal.objects.filter(announcement=announcement))
            session = self.get_session_data()
            self.assertFalse(session.get("excluded_announcements", False))

    def test_ajax_dismiss_session(self):
        """
        Ensure we dismiss Announcement from the session via AJAX.
        """
        announcement = Announcement.objects.create(
            title="Election Results",
            content="some results",
            creator=self.staff,
            dismissal_type=Announcement.DISMISSAL_SESSION
        )
        announcement.save()

        # Create user without "can_manage" permission.
        user = self.make_user("user")
        with self.login(user):
            self.post(
                "pinax_announcements:announcement_dismiss",
                pk=announcement.pk,
                extra=dict(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            )
            self.response_200()
            self.assertFalse(Dismissal.objects.filter(announcement=announcement))
            session = self.get_session_data()
            excluded = session.get("excluded_announcements", False)
            self.assertTrue(excluded)
            self.assertEqual(excluded, [announcement.pk])

    def test_ajax_dismiss_permanent(self):
        """
        Ensure we dismiss Announcement permanently via AJAX.
        """
        announcement = Announcement.objects.create(
            title="Election Results",
            content="some results",
            creator=self.staff,
            dismissal_type=Announcement.DISMISSAL_PERMANENT
        )
        announcement.save()

        # Create user without "can_manage" permission.
        user = self.make_user("user")
        with self.login(user):
            self.post(
                "pinax_announcements:announcement_dismiss",
                pk=announcement.pk,
                extra=dict(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            )
            self.response_200()
            self.assertTrue(Dismissal.objects.filter(announcement=announcement))
            session = self.get_session_data()
            self.assertFalse(session.get("excluded_announcements", False))

    def test_list(self):
        """
        Ensure Announcement list appears for user with "can_manage" perm.
        """
        announcement = Announcement.objects.create(
            title="Election Results",
            content="some results",
            creator=self.staff
        )
        announcement.save()

        with self.login(self.staff):
            self.get("pinax_announcements:announcement_list")
            self.response_200()
            self.assertSequenceEqual(self.last_response.context["object_list"], [announcement])

    def test_delete(self):
        """
        Ensure Announcement is deleted.
        """
        announcement = Announcement.objects.create(
            title="Election Results",
            content="some results",
            creator=self.staff
        )
        announcement.save()

        with self.login(self.staff):
            self.post("pinax_announcements:announcement_delete", pk=announcement.pk, follow=True)
            self.response_200()
            self.assertFalse(Announcement.objects.filter(pk=announcement.pk))
