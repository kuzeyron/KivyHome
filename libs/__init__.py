from functools import partial
from os.path import abspath, dirname, join

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import DictProperty, NumericProperty, ObjectProperty
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

from libs.favorite_apps_configuration import (retrieve_favorite_apps,
                                              store_favorite_apps)
from libs.startup import Startup
from libs.utils import importer
from libs.wallpaper import wallpaper

Builder.load_file(join('kv', f'{platform}.kv'))

__all__ = ('KivyHome', )

if platform != 'android':
    from kivy.metrics import dp
    Window.size = dp(950), dp(700)
    Logger.debug("Application is not Android.")


class Basement(BoxLayout):
    pass


class KivyHome(App, Startup):
    bg = ObjectProperty(None, allownone=True, rebind=True)
    desktop_icons = DictProperty()

    def build(self):
        self.desktop_icons = retrieve_favorite_apps()
        self.bind(desktop_icons=self.store_desktop_data)
        self.bg = wallpaper(f'assets/wallpapers/background_{platform}.jpeg')

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
