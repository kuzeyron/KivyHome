from importlib import import_module

from kivy.logger import Logger
from kivy.utils import platform

__all__ = ['vibrate', ]


def vibrate(duration):
    if platform in {'android'}:
        jnius = import_module('jnius')
        autoclass = jnius.autoclass

        Context = autoclass('android.content.Context')
        PythonActivity = autoclass(
            'org.kivy.android.PythonActivity'
        )
        activity = PythonActivity.mActivity
        vibrator = activity.getSystemService(
            Context.VIBRATOR_SERVICE
        )

        vibrator.vibrate(duration * 1000)

        return vibrator

    Logger.debug("Vibrator function is only supported on Android devices.")

    class FakeVib:
        def vibrate(self, *largs) -> None:
            pass

        def cancel(self, *largs) -> None:
            pass

    return FakeVib()
