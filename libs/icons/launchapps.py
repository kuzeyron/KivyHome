from importlib import import_module
from subprocess import STDOUT, check_output

from kivy.logger import Logger
from kivy.utils import platform

__all__ = ('launch_app', )

def execute_command(cmd: list) -> str:
    return check_output(cmd, encoding='utf8', stderr=STDOUT)


def launch_app(package: str) -> None:
    Logger.debug("[KivyHome] Attempt on running the package %s", package)
    if platform == 'android':
        jnius = import_module('jnius')
        autoclass = jnius.autoclass
        cast = jnius.cast
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        context = cast('android.content.Context',
                       PythonActivity.mActivity)
        pm = context.getPackageManager()
        launcher = pm.getLaunchIntentForPackage(package)
        activity.startActivity(launcher)
    elif platform == 'linux':
        execute_command(['gtk-launch', package])
    else:
        Logger.debug("[KivyHome] Launching apps is only supported on Linux/Android devices")
