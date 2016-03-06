from django.template import Template

from ..models import Announcement
from ..signals import (
    announcement_created,
    announcement_deleted,
    announcement_updated,
)
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

        self.title_string = "Election Results"
        self.announcement = Announcement.objects.create(
            title=self.title_string,
            content="some results",
            creator=self.staff
        )
        self.announcement.save()


class TestViews(BaseTest):

    def test_list_without_can_manage(self):
        """
        Ensure Announcement list DOES NOT appear for user without "can_manage" perm.
        """
        # Create user without "can_manage" permission.
        user = self.make_user("user")
        with self.login(user):
            self.get("pinax_announcements:announcement_list")
            self.response_302()

    def test_list(self):
        """
        Ensure Announcement list appears for user with "can_manage" perm.
        """
        with self.login(self.staff):
            self.get("pinax_announcements:announcement_list")
            self.response_200()
            self.assertInContext("object_list")
            self.assertSequenceEqual(
                self.last_response.context["object_list"],
                [self.announcement]
            )

    def test_detail_without_can_manage(self):
        """
        Ensure Announcement appears in detail view context for user without "can_manage" perm.
        """
        user = self.make_user("user")
        with self.login(user):
            self.get("pinax_announcements:announcement_detail", pk=self.announcement.pk)
            self.response_200()
            self.assertContext("announcement", self.announcement)

    def test_detail(self):
        """
        Ensure Announcement appears in detail view context.
        """
        with self.login(self.staff):
            self.get("pinax_announcements:announcement_detail", pk=self.announcement.pk)
            self.response_200()
            self.assertContext("announcement", self.announcement)

    def test_create(self):
        """
        Create an Announcement
        """
        title_string = "Acme Recalls Rocket Sled"
        post_args = {
            "title": title_string,
            "content": "Wile E. Coyote crashed",
            "dismissal_type": "2",
            "publish_start": "2016-03-06",
        }

        def receiver(sender, **kwargs):
            self.assertTrue("announcement" in kwargs)
            self.assertTrue('request' in kwargs)
            received_signals.append(kwargs.get('signal'))

        received_signals = []
        announcement_created.connect(receiver)

        with self.login(self.staff):
            self.post("pinax_announcements:announcement_create", data=post_args, follow=True)
            self.response_200()
            self.assertTrue(Announcement.objects.get(title=title_string))

            self.assertEqual(len(received_signals), 1)
            self.assertEqual(received_signals, [announcement_created])

    def test_update(self):
        """
        Update existing Announcement
        """
        title_string = "Acme Recalls Rocket Sled"
        post_args = {
            "title": title_string,
            "content": "Wile E. Coyote crashed",
            "dismissal_type": "2",
            "publish_start": "2016-03-06",
        }

        def receiver(sender, **kwargs):
            self.assertTrue("announcement" in kwargs)
            self.assertTrue('request' in kwargs)
            received_signals.append(kwargs.get('signal'))

        received_signals = []
        announcement_updated.connect(receiver)

        with self.login(self.staff):
            self.post(
                "pinax_announcements:announcement_update",
                pk=self.announcement.pk,
                data=post_args,
                follow=True
            )
            self.response_200()
            announcement = Announcement.objects.get(title=title_string)
            self.assertEqual(announcement.pk, self.announcement.pk)
            self.assertFalse(Announcement.objects.filter(title=self.title_string))

            self.assertEqual(len(received_signals), 1)
            self.assertEqual(received_signals, [announcement_updated])

    def test_delete(self):
        """
        Delete an Announcement
        """
        self.assertTrue(Announcement.objects.filter(pk=self.announcement.pk))

        def receiver(sender, **kwargs):
            self.assertTrue("announcement" in kwargs)
            self.assertTrue('request' in kwargs)
            received_signals.append(kwargs.get('signal'))

        received_signals = []
        announcement_deleted.connect(receiver)

        with self.login(self.staff):
            self.post(
                "pinax_announcements:announcement_delete",
                pk=self.announcement.pk,
                follow=True
            )
            self.response_200()
            self.assertFalse(Announcement.objects.filter(pk=self.announcement.pk))

            self.assertEqual(len(received_signals), 1)
            self.assertEqual(received_signals, [announcement_deleted])

    def test_dismiss(self):
        """
        Dismiss an Announcement
        """
        pass
