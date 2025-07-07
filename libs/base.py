from kivy.properties import (ColorProperty, DictProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.boxlayout import BoxLayout

from .favorite_apps_configuration import (retrieve_favorite_apps,
                                          store_favorite_apps)
from .wallpaper import wallpaper

__all__ = ('KivyHome', )

class KivyHome(BoxLayout):
    _instance: object = None
    _initialized: bool = False
    _background_texture = ObjectProperty(None, allownone=True)
    background_color = ColorProperty((.243, .258, .27, 1))
    background_path = StringProperty('assets/wallpapers/default_wallpaper.jpeg', allownone=True)
    desktop_icons = DictProperty()

    def __init__(self, **kwargs):
        if not self._initialized:  # init once
            super().__init__(**kwargs)
            self._initialized = True

    def on_kv_post(self, instance=None, value=None):
        if not self._background_texture:
            self.on_background_path()
        self.desktop_icons = retrieve_favorite_apps()
        self.bind(desktop_icons=self.store_desktop_data)

    def store_desktop_data(self, instance=None, value=None):
        store_favorite_apps(config=self.desktop_icons)

    def change_direction(self, orientation: str = 'up', target: str = 'main'):
        manager = self.ids.home_screen_manager
        manager.transition.direction = orientation
        manager.current = target

        return True

    def on_background_path(self, instance=None, background_path=None):
        if background_path or self.background_path:
            self._background_texture = wallpaper(self.background_path)
        else:
            self._background_texture = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            from os.path import dirname, join
            from kivy.lang import Builder
            from kivy.utils import platform

            # Code executed right here prevents Kivy from circular imports
            Builder.load_file(join(dirname(__file__), 'kv', f'{platform}.kv'))
            cls._instance = super().__new__(cls)

        return cls._instance
