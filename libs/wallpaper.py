from os import makedirs, stat
from os.path import basename, dirname, isfile, join

from kivy.core.image import Image
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.properties import (ColorProperty, ListProperty, ObjectProperty,
                             OptionProperty, StringProperty)
from kivy.utils import platform

__all__ = ('WallpaperHandler', 'wallpaper')

DEFAULT_PATH = join(dirname(__file__), 'assets/wallpapers/default_wallpaper.jpeg')

if platform == 'android':
    from android.storage import app_storage_path
else:
    import sys

    def app_storage_path():
        return sys.path[0]


def _cut(texture=None, crop: list = None):
    crop = crop or Window.size

    target_ratio = crop[0] / crop[1]
    texture_ratio = texture.width / float(texture.height)

    if texture_ratio > target_ratio:
        new_width = texture.height * target_ratio
        new_height = texture.height
        x_offset = (texture.width - new_width) / 2
        y_offset = 0
        Logger.debug('[KivyHome] Wallpaper: Cropping horizontally. {texture.size=%s} to {crop=%s}', texture.size, (new_width, new_height))
    elif texture_ratio < target_ratio:
        new_width = texture.width
        new_height = texture.width / target_ratio
        x_offset = 0
        y_offset = (texture.height - new_height) / 2
        Logger.debug('[KivyHome] Wallpaper: Cropping vertically. {texture.size=%s} to {crop=%s}', texture.size, (new_width, new_height))
    else:
        Logger.debug("[KivyHome] Wallpaper: No cropping needed (aspect ratios match).")

        return texture

    return texture.get_region(x=x_offset,
                              y=y_offset,
                              width=new_width,
                              height=new_height)


def wallpaper(source: str, crop: list = None, reset: bool = None):
    cache_folder = join(app_storage_path(), '.cache', 'wallpapers')
    filesize = stat(source).st_size
    filename = f"{filesize};{basename(source)}"
    path = join(cache_folder, filename)
 
    if not reset and isfile(path):
        Logger.debug("[KivyHome] Wallpaper: Re-using cached wallpaper at %s", path)

        return Image(path).texture

    texture = Image(source).texture

    if platform == 'android':
        texture = _cut(texture, crop)
        makedirs(cache_folder, exist_ok=True)
        texture.save(path, flipped=False)
        Logger.debug("[KivyHome] Wallpaper: Stored the cropped wallpaper at %s", path)

    return texture


class WallpaperHandler(EventDispatcher):
    color = ColorProperty((.243, .258, .27, 1))
    fit_mode = OptionProperty('free', options=('free', 'fit'))
    path = StringProperty(DEFAULT_PATH, allownone=True)
    texture = ObjectProperty(None, allownone=True)
    scaled_size = ListProperty((0, 0))
    scaled_pos = ListProperty((0, 0))

    def _apply_wallpaper(self, _=None, path=None):
        if _path := path or self.path:
            self.texture = wallpaper(_path)
            self.scaled_size = self.texture.size
        else:
            self.texture = None
            self.scaled_size = self.size

        self.on_center(center_pos=self.center)

    def on_center(self, _=None, center_pos=None):
        if self.texture is not None and self.fit_mode == 'free':
            self.scaled_pos = (center_pos[0] - self.texture.width / 2,
                               center_pos[1] - self.texture.height / 2)
        elif self.texture is not None and self.fit_mode == 'fit':
            widget_width, widget_height = self.size
            texture_width, texture_height = self.texture.size
            texture_aspect_ratio = texture_width / float(texture_height)
            scaled_height_by_width = widget_width / texture_aspect_ratio
            scaled_width_by_height = widget_height * texture_aspect_ratio

            if scaled_height_by_width <= widget_height:
                self.scaled_size = widget_width, scaled_height_by_width
            else:
                self.scaled_size = scaled_width_by_height, widget_height
            self.scaled_pos = (center_pos[0] - self.scaled_size[0] / 2,
                               center_pos[1] - self.scaled_size[1] / 2)
        else:
            self.scaled_pos = self.pos
