from importlib import import_module

from kivy.logger import Logger
from kivy.utils import platform

__all__ = ['launch_app', ]

def launch_app(package):
    if platform in {'android'}:
        jnius = import_module('jnius')
        autoclass = jnius.autoclass
        cast = jnius.cast
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        context = cast('android.content.Context',
                       PythonActivity.mActivity)
        pm = context.getPackageManager()
        launcher = pm.getLaunchIntentForPackage(package);
        activity.startActivity(launcher)

    else:
        Logger.debug("Launching apps is only supported on Android devices.")
