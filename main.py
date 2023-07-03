from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import DictProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

from libs.android_hide_system_bars import HideBars
from libs.favorite_apps import retrieve_favorite_apps, store_favorite_apps
from libs.wallpaper import wallpaper

if platform not in {'android', 'ios'}:
    from kivy.core.window import Window
    from kivy.metrics import dp
    Window.size = dp(400), dp(660)
    Logger.debug("Application is not Android.")


class Basement(BoxLayout):
    pass


class KivyHome(App, HideBars):
    bg = ObjectProperty(None, allownone=True)
    desktop_icons = DictProperty()

    def build(self):
        self.desktop_icons = retrieve_favorite_apps()
        self.bind(desktop_icons=self.store_desktop_data)
        self.bg = wallpaper('assets/wallpapers/city.jpg')

        return Basement()

    def store_desktop_data(self, *largs):
        store_favorite_apps(config=self.desktop_icons)

    def on_resume(self):
        Clock.schedule_once(partial( self.change_target, 'up', 'main'), 0)

        return True

    def change_target(self, orientation, target, *largs):
        manager = self.root.ids.sm
        manager.transition.direction = orientation
        manager.current = target

        return True


if __name__ == '__main__':
    KivyHome().run()
