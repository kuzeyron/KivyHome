from kivy.logger import Logger
from kivy.utils import platform

__all__ = ('vibrate', )

class FakeVib:
    def vibrate(self, duration=None):
        pass

    def cancel(self, extra=None):
        pass


def vibrate(duration):
    if platform in {'android'}:
        from jnius import autoclass

        Context = autoclass('android.content.Context')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        vibrator = activity.getSystemService(Context.VIBRATOR_SERVICE)

        vibrator.vibrate(duration * 1000)

        return vibrator

    Logger.debug("Vibrator function is only supported on Android devices.")

    return FakeVib()
