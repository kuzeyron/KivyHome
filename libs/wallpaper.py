import sys
from os import makedirs, stat, remove
from os.path import basename, dirname, isfile, join

from kivy.core.image import Image
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.properties import (ColorProperty, ListProperty, ObjectProperty,
                             OptionProperty, StringProperty)
from kivy.utils import platform

__all__ = ('texture_cutter', 'get_wallpaper_texture', 'WallpaperHandler')

DEFAULT_PATH = join(dirname(__file__), 'assets/wallpapers/default_wallpaper.jpeg')
STORAGE_PATH = sys.path[0]

if platform == 'android':
    from android.storage import app_storage_path
    STORAGE_PATH = app_storage_path()


def texture_cutter(texture: object = None, crop_region: list = None) -> object:
    crop_region = crop_region or Window.size

    target_ratio = crop_region[0] / crop_region[1]
    texture_ratio = texture.width / float(texture.height)

    if texture_ratio > target_ratio:
        new_width = texture.height * target_ratio
        new_height = texture.height
        x_offset = (texture.width - new_width) / 2
        y_offset = 0
        Logger.debug('[KivyHome] Cropping wallpaper horizontally')
    elif texture_ratio < target_ratio:
        new_width = texture.width
        new_height = texture.width / target_ratio
        x_offset = 0
        y_offset = (texture.height - new_height) / 2
        Logger.debug('[KivyHome] Cropping wallpaper vertically')
    else:
        Logger.debug("[KivyHome] No cropping needed for wallpaper (aspect ratios match).")

        return texture

    return texture.get_region(x=x_offset,
                              y=y_offset,
                              width=new_width,
                              height=new_height)


def get_wallpaper_texture(image_source: str, crop_region: list = None, force_recreate: bool = False, fit_mode: str = 'free'):
    wallpaper_cache_dir = join(STORAGE_PATH, '.cache', 'wallpapers')
    source_file_size = stat(image_source).st_size
    cached_filename = f"{source_file_size};{basename(image_source)}"
    cached_wallpaper_path = join(wallpaper_cache_dir, cached_filename)
    is_cached_wallpaper_valid = isfile(cached_wallpaper_path)

    if not force_recreate and is_cached_wallpaper_valid and fit_mode != 'free':
        Logger.debug("[KivyHome] Re-using cached wallpaper from %s", cached_wallpaper_path)
        return Image(cached_wallpaper_path).texture
    elif fit_mode == 'free' and is_cached_wallpaper_valid:
        Logger.debug("[KivyHome] Removing old cached image for 'free' fit mode: %s",
                     cached_wallpaper_path)
        remove(cached_wallpaper_path)

    wallpaper_texture = Image(image_source).texture

    if platform == 'android' and fit_mode != 'free':
        wallpaper_texture = texture_cutter(wallpaper_texture, crop_region)
        makedirs(wallpaper_cache_dir, exist_ok=True)
        wallpaper_texture.save(cached_wallpaper_path, flipped=False)
        Logger.debug("[KivyHome] Stored the (cropped) wallpaper at %s",
                     cached_wallpaper_path)

    return wallpaper_texture


class WallpaperHandler(EventDispatcher):
    _scaled_pos = ListProperty((0, 0))
    _scaled_size = ListProperty((0, 0))
    _texture = ObjectProperty(None, allownone=True)
    background_path = StringProperty(DEFAULT_PATH, allownone=True)
    color = ColorProperty((.243, .258, .27, 1))
    fit_mode = OptionProperty('free', options=('free', 'fit'))

    def on_fit_mode(self, _: object = None, mode: str = None):
        self.on_background_path()

    def on_background_path(self, _: object = None, path: str = None) -> None:
        if _path := path or self.background_path:
            self._texture = get_wallpaper_texture(_path, fit_mode=self.fit_mode)
            self._scaled_size = self._texture.size
        else:
            Logger.debug("[KivyHome] No wallpapers will be used")
            self._texture = None
            self._scaled_size = self.size

        self.on_center(center_pos=self.center)

    def on_center(self, _: object = None, center_pos: list = None) -> None:
        if self._texture is not None and self.fit_mode == 'free':
            self._scaled_pos = (center_pos[0] - self._texture.width / 2,
                                center_pos[1] - self._texture.height / 2)
        elif self._texture is not None and self.fit_mode == 'fit':
            widget_width, widget_height = self.size
            texture_width, texture_height = self._texture.size
            texture_aspect_ratio = texture_width / float(texture_height)
            scaled_height_by_width = widget_width / texture_aspect_ratio
            scaled_width_by_height = widget_height * texture_aspect_ratio

            if scaled_height_by_width <= widget_height:
                self._scaled_size = widget_width, scaled_height_by_width
            else:
                self._scaled_size = scaled_width_by_height, widget_height
            self._scaled_pos = (center_pos[0] - self._scaled_size[0] / 2,
                                center_pos[1] - self._scaled_size[1] / 2)
