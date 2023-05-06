from kivy.app import App
from kivy.logger import Logger
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

from libs.android_hide_system_bars import HideBars
from libs.wallpaper import wallpaper

if platform not in {'android', 'ios'}:
    from kivy.core.window import Window
    from kivy.metrics import dp
    Window.size = dp(400), dp(650)
    Logger.debug("Application is not Android.")


class Basement(BoxLayout):
    pass


class KivyHome(App, HideBars):
    bg = ObjectProperty(None, allownone=True)
    desktop_icons = ListProperty(['org.test.fake2', 'org.test.fake5', 'com.android.settings',
                                  'com.huawei.camera', 'in.krosbits.musicolet', 'org.kuzeyron.eyesight',
                                  'com.discord', 'com.ebay.mobile', 'com.github.android',
                                  'org.mozilla.firefox', 'com.radiolight.suede', 'com.ninegag.android.app',
                                  'com.imdb.mobile'])

    def build(self):
        self.bg = wallpaper('assets/wallpapers/city.jpg')
        return Basement()

    def change_target(self, orientation, target, *largs):
        manager = self.root.ids.sm
        manager.transition.direction = orientation
        manager.current = target


if __name__ == '__main__':
    KivyHome().run()
