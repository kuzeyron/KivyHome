from importlib import import_module

from kivy.core.window import Window
from kivy.logger import Logger

__all__ = ('Startup', )

CUTOUT_HEIGHT = 0.
NAVBAR_HEIGHT = 0.
STATBAR_HEIGHT = 0.

run_on_ui_thread = import_module('android.runnable').run_on_ui_thread
jnius = import_module('jnius')
autoclass = jnius.autoclass

AndroidView = autoclass('android.view.View')
mActivity = import_module('android').mActivity

try:
    decorview = mActivity.getWindow().getDecorView()
    cutout = decorview.rootWindowInsets.displayCutout
    rect = cutout.boundingRects.get(0)

    if CUTOUT_HEIGHT := float(rect.height()):
        # Code by AnshDadwal
        displayMetrics = autoclass('android.util.DisplayMetrics')
        mActivity.getWindowManager().getDefaultDisplay().getMetrics(displayMetrics())
        resources = mActivity.getResources()
        resourceId = resources.getIdentifier('status_bar_height', 'dimen', 'android')
        STATBAR_HEIGHT = float(resources.getDimensionPixelSize(resourceId))
        resourceId = resources.getIdentifier('navigation_bar_height', 'dimen', 'android')
        NAVBAR_HEIGHT = float(resources.getDimensionPixelSize(resourceId)
                              if resourceId > 0 else 0)

except Exception:
    pass

@run_on_ui_thread
def android_hide_system_bars():
    decorview.setSystemUiVisibility(
        AndroidView.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
        AndroidView.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
        AndroidView.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
    )


class Startup:
    cutout_height = CUTOUT_HEIGHT
    navbar_height = NAVBAR_HEIGHT
    statbar_height = STATBAR_HEIGHT

    def __init__(self, **kwargs):
        Window.bind(on_keyboard=self.key_press)

    def on_start(self):
        android_hide_system_bars()

    def key_press(self, w, k, *lr):
        if there := k in {27} and platform in {'android'}:
            manager = self.root.ids.sm
            manager.transition.direction = 'up'
            manager.current = 'main'

        return there
