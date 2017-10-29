try:
    from django.urls import reverse, reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse, reverse_lazy  # noqa

try:
    from unittest import mock
except ImportError:
    import mock  # noqa
