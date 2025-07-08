from kivy.app import App
from kivy.properties import (ColorProperty, DictProperty, ListProperty,
                             ObjectProperty, StringProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

from .favorite_apps_configuration import (retrieve_favorite_apps,
                                          store_favorite_apps)
from .wallpaper import wallpaper

__all__ = ('KivyHome', )

class KivyHome(BoxLayout):
    _background_texture = ObjectProperty(None, allownone=True)
    _initialized: bool = False
    _instance: object = None
    background_color = ColorProperty((.243, .258, .27, 1))
    background_path = StringProperty('assets/wallpapers/default_wallpaper.jpeg', allownone=True)
    cutout_supported_bar_heights = ListProperty((0, 0))
    desktop_icons = DictProperty()

    def __init__(self, **kwargs):
        if not self._initialized:  # init once
            self._initialized = True
            super().__init__(**kwargs)

    def on_kv_post(self, instance=None, value=None):
        if not self._background_texture:
            self.on_background_path()
        self.display_cutout_supported()
        self.desktop_icons = retrieve_favorite_apps()
        self.bind(desktop_icons=self.store_desktop_data)

    def store_desktop_data(self, instance=None, value=None):
        store_favorite_apps(config=self.desktop_icons)

    def change_direction(self, dt=None, orientation: str = 'up', target: str = 'main'):
        manager = self.ids.home_screen_manager
        manager.transition.direction = orientation
        manager.current = target

        return True

    def display_cutout_supported(self, dt=None):
        if platform == 'android':
            from android.display_cutout import get_height_of_bar

            if isinstance(App.get_running_app().root, KivyHome):
                self.cutout_supported_bar_heights = [get_height_of_bar('status'),
                                                     get_height_of_bar('navigation')]

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
