from importlib import import_module
from subprocess import STDOUT, check_output

from kivy.logger import Logger
from kivy.utils import platform

__all__ = ['launch_app', ]

def execute_command(cmd):
    return check_output(cmd, encoding='utf8', stderr=STDOUT)


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
    elif platform in {'linux'}:
        execute_command(['gtk-launch', package])
    else:
        Logger.debug("Launching apps is only supported on Linux/Android devices.")
