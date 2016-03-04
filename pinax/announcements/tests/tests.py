from django.template import (
##    Context,
    Template,
)

from ..models import (
    Announcement,
##    Dismissal,
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

        title_string = "Election Results"
        self.announcement = Announcement.objects.create(
            title=title_string,
            content="some results",
            creator=self.staff
        )
        self.announcement.save()


class TestViews(BaseTest):

    def test_list(self):
        """
        Ensure Announcement list does not appear for user without "can_manage" perm.
        """
        # Create user without "can_manage" permission.
        user = self.make_user("user")
        with self.login(user):
            self.get("pinax_announcements:announcement_list")
            self.response_302()

    def test_can_manage_list(self):
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

    def test_detail(self):
        """
        Ensure Announcement appears in detail view context.
        """
        with self.login(self.staff):
            self.get("pinax_announcements:announcement_detail", pk=self.announcement.pk)
            self.response_200()
            self.assertInContext("announcement")
            self.assertContext("announcement", self.announcement)
