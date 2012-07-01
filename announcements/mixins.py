from django.conf import settings
from django.utils.importlib import import_module


def _resolve(mixin_setting):
    if isinstance(mixin_setting, basestring):
        try:
            mod_name, klass_name = mixin_setting.rsplit(".", 1)
        except ValueError:
            raise Exception("Improperly configured.")
        try:
            mod = import_module(mod_name)
        except ImportError:
            raise Exception("Could not import %s" % mod_name)
        try:
            klass = getattr(mod, klass_name)
        except AttributeError:
            raise Exception("The module '%s' does not contain '%s'." % (mod_name, klass_name))
        mixin_setting = klass
    return mixin_setting


class DefaultProtectedMixin(object):
    
    pass


ProtectedMixin = _resolve(
    getattr(settings, "ANNOUNCEMENTS_PROTECTED_MIXIN", DefaultProtectedMixin)
)
