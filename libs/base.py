from kivy.properties import DictProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from libs.favorite_apps_configuration import (retrieve_favorite_apps,
                                              store_favorite_apps)
from libs.wallpaper import wallpaper

__all__ = ('KivyHome', )

class KivyHome(BoxLayout):
    _instance: object = None
    _initialized: bool = False
    background_texture = ObjectProperty(None, allownone=True, rebind=True)
    desktop_icons = DictProperty()

    def __init__(self, **kwargs):
        if not self._initialized:
            super().__init__(**kwargs)
            self.desktop_icons = retrieve_favorite_apps()
            self.bind(desktop_icons=self.store_desktop_data)
            self.background_texture = wallpaper(f'assets/wallpapers/background_{platform}.jpeg')
            self._initialized = True

    def store_desktop_data(self):
        store_favorite_apps(config=self.desktop_icons)

    def change_target(self, orientation, target, *largs):
        manager = self.ids.sm
        manager.transition.direction = orientation
        manager.current = target

        return True

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            from os.path import dirname, join
            from kivy.lang import Builder

            Builder.load_file(join(dirname(__file__), 'kv', f'{platform}.kv'))
            cls._instance = super().__new__(cls)

        return cls._instance


if __name__ == '__main__':
    KivyHome().run()
