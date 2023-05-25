import django.dispatch

announcement_created = django.dispatch.Signal()
announcement_updated = django.dispatch.Signal()
announcement_deleted = django.dispatch.Signal()
