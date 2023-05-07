from kivy.app import App
from kivy.logger import Logger
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

from libs.android_hide_system_bars import HideBars
from libs.favorite_apps import retrieve_favorite_apps, store_favorite_apps
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
    desktop_icons = ListProperty()

    def build(self):
        self.desktop_icons = retrieve_favorite_apps()
        self.bind(desktop_icons=self.store_favorites)
        self.bg = wallpaper('assets/wallpapers/city.jpg')
        return Basement()

    def store_favorites(self, *largs):
        self.desktop_icons = store_favorite_apps(config=self.desktop_icons)

    def change_target(self, orientation, target, *largs):
        manager = self.root.ids.sm
        manager.transition.direction = orientation
        manager.current = target


if __name__ == '__main__':
    KivyHome().run()
