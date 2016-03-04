import os

from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.template import (
    Context,
    Template,
)

from ..models import (
    Announcement,
    Dismissal,
)
from .test import TestCase


class TestCaseMixin(object):

    def assert_renders(self, tmpl, context, value):
        tmpl = Template(tmpl)
        self.assertEqual(tmpl.render(context).strip(), value)


class BaseTest(TestCase, TestCaseMixin):
    def setUp(self):
        self.staff = self.make_user("staff")
        self.staff.is_staff = True
        self.staff.save()
        self.assertTrue(self.staff.has_perm("announcements.can_manage"))

        if hasattr(self, "template_dirs"):
            self._old_template_dirs = settings.TEMPLATE_DIRS
            settings.TEMPLATE_DIRS = self.template_dirs

    def tearDown(self):
        if hasattr(self, "_old_template_dirs"):
            settings.TEMPLATE_DIRS = self._old_template_dirs


class TestViews(BaseTest):
    template_dirs = [
        os.path.join(os.path.dirname(__file__), "templates")
    ]

    def test_list(self):
        """
        Ensure Announcement list does not appear for user without "can_manage" perm.
        """
        title_string = "Election Results"
        announcement = Announcement.objects.create(
            title=title_string,
            content="some results",
            creator=self.staff
        )
        announcement.save()

        # Create user without "can_manage" permission.
        user = self.make_user("user")
        with self.login(user):
            response = self.get("pinax_announcements:announcement_list")
            self.response_302()

    def test_can_manage_list(self):
        """
        Ensure Announcement list appears for user with "can_manage" perm.
        """
        title_string = "Election Results"
        announcement = Announcement.objects.create(
            title=title_string,
            content="some results",
            creator=self.staff
        )
        announcement.save()

        with self.login(self.staff):
            response = self.get("pinax_announcements:announcement_list")
            self.response_200()
            self.assertContains(response, title_string)

##    def test_get_message_create(self):
##        """
##        Ensure user can get page to create a message.
##        """
##        with self.login(self.brosner):
##            response = self.get("pinax_messages_message_create")
##            self.assertEqual(response.status_code, 200)
##
##    def test_post_message_create(self):
##        """
##        Ensure proper inbox counts when a message is sent.
##        """
##        with self.login(self.brosner):
##            data = {
##                "subject": "The internet is down.",
##                "content": "Does this affect any of our sites?",
##                "to_user": str(self.jtauber.id)
##            }
##            response = self.post("pinax_messages_message_create", data=data)
##            self.assertEqual(response.status_code, 302)
##            self.assertEqual(Thread.inbox(self.jtauber).count(), 1)
##            self.assertEqual(Thread.inbox(self.brosner).count(), 0)
##
##    def test_get_message_user_create(self):
##        """
##        Ensure form selects correct message recipient.
##        """
##        with self.login(self.brosner):
##            response = self.get("pinax_messages_message_user_create", user_id=self.jtauber.id)
##            self.assertEqual(response.status_code, 200)
##            self.assertContains(response, "selected=\"selected\">jtauber</option>")
##
##    def test_sender_get_thread_detail(self):
##        """
##        Ensure message sender can view thread detail.
##        """
##        message_string = "Avast ye landlubbers"
##        Message.new_message(
##            self.brosner, [self.jtauber], "Anything", message_string)
##
##        thread_id = Thread.inbox(self.jtauber).get().id
##        with self.login(self.brosner):
##            response = self.get("pinax_messages_thread_detail", pk=thread_id)
##            self.assertEqual(response.status_code, 200)
##            self.assertContains(response, message_string)
##
##    def test_recipient_get_thread_detail(self):
##        """
##        Ensure message recipient can view thread detail.
##        """
##        message_string = "Avast ye landlubbers"
##        Message.new_message(
##            self.brosner, [self.jtauber], "Anything", message_string)
##
##        thread_id = Thread.inbox(self.jtauber).get().id
##        with self.login(self.jtauber):
##            response = self.get("pinax_messages_thread_detail", pk=thread_id)
##            self.assertEqual(response.status_code, 200)
##            self.assertContains(response, message_string)
##
##    def test_post_thread_delete(self):
##        """
##        Ensure a thread can be deleted by the recipient.
##        """
##        Message.new_message(
##            self.brosner, [self.jtauber], "Anything", "and everything")
##
##        thread_id = Thread.inbox(self.jtauber).get().id
##        with self.login(self.jtauber):
##            response = self.post("pinax_messages_thread_delete", pk=thread_id)
##            self.assertEqual(response.status_code, 302)
##            self.assertEqual(Thread.inbox(self.jtauber).count(), 0)
##
##    def test_post_thread_detail(self):
##        """
##        Ensure by replying to a message the thread is marked as read.
##        """
##        data = {
##            "content": "Nope, the internet being down doesn't affect us.",
##        }
##        Message.new_message(
##            self.brosner, [self.jtauber], "Anything", "and everything")
##        # jtauber has one unread message
##        self.assertEqual(Thread.unread(self.jtauber).count(), 1)
##
##        thread_id = Thread.inbox(self.jtauber).get().id
##        with self.login(self.jtauber):
##            # jtauber replies to the message...
##            response = self.post("pinax_messages_thread_detail", pk=thread_id, data=data)
##            self.assertEqual(response.status_code, 302)
##            self.assertEqual(Thread.inbox(self.brosner).count(), 1)
##            self.assertEqual(
##                Thread.inbox(self.brosner).get().messages.count(),
##                2
##            )
##            # ...and by replying implies the original message was read.
##            self.assertEqual(Thread.unread(self.jtauber).count(), 0)
##
##
##class TestTemplateTags(BaseTest):
##    def test_unread(self):
##        """
##        Ensure `unread` template_tag produces correct results.
##        """
##        thread = Message.new_message(
##            self.brosner,
##            [self.jtauber],
##            "Why did you break the internet?", "I demand to know.").thread
##        tmpl = """
##               {% load pinax_messages_tags %}
##               {% if thread|unread:user %}UNREAD{% else %}READ{% endif %}
##               """
##        self.assert_renders(
##            tmpl,
##            Context({"thread": thread, "user": self.jtauber}),
##            "UNREAD"
##        )
##        self.assert_renders(
##            tmpl,
##            Context({"thread": thread, "user": self.brosner}),
##            "READ",
##        )
