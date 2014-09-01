from django.db.models.signals import class_prepared
from django.utils import six
from django.conf import settings


try:
    from django.contrib.auth import get_user_model as auth_get_user_model
except ImportError:
    auth_get_user_model = None
    from django.contrib.auth.models import User


AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


def get_user_model(*args, **kwargs):
    if auth_get_user_model is not None:
        return auth_get_user_model(*args, **kwargs)
    else:
        return User
