from kivy.app import App
from kivy.clock import Clock
from kivy.properties import (DictProperty, NumericProperty)
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform

from .favorite_apps_configuration import (retrieve_favorite_apps,
                                          store_favorite_apps)
from .wallpaper import WallpaperHandler

__all__ = ('KivyHome', )

class KivyHome(WallpaperHandler, ScreenManager):
    _initialized: bool = False
    _instance: object = None
    desktop_icons = DictProperty()
    navigation_bar_height = NumericProperty()
    status_bar_height = NumericProperty()

    def __init__(self, **kwargs) -> None:
        if not self._initialized:  # init once
            self._initialized = True
            super().__init__(**kwargs)
            Clock.schedule_once(self._setup, 0)

    def _store_desktop_data(self, instance=None, value=None) -> None:
        store_favorite_apps(config=self.desktop_icons)

    def change_direction(self, dt=None, orientation: str = 'up', target: str = 'main') -> None:
        self.transition.direction, self.current = orientation, target

    def _setup(self, dt: float = None) -> None:
        self._apply_wallpaper()
        self.desktop_icons = retrieve_favorite_apps()
        self.bind(desktop_icons=self._store_desktop_data)

        if platform == 'android' and isinstance(App.get_running_app().root, KivyHome):
            from android.display_cutout import get_cutout_mode, get_heights_of_both_bars
            if get_cutout_mode() not in {None, 'never'}:
                self.status_bar_height, self.navigation_bar_height = get_heights_of_both_bars()

    def __new__(cls: object, *args, **kwargs) -> object:
        if not cls._instance:
            from os.path import dirname, join
            from kivy.lang import Builder

            # Code executed right here prevents Kivy from circular imports
            Builder.load_file(join(dirname(__file__), 'kivyhome.kv'))
            cls._instance = super().__new__(cls)

        return cls._instance
