from os import makedirs, stat
from os.path import basename, isfile, join

from kivy.core.image import Image
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.utils import platform

__author__ = 'cheaterman and kuzeyron'
__all__ = ('wallpaper', )

if platform == 'android':
    from android.storage import app_storage_path
else:
    import sys

    def app_storage_path():
        return sys.path[0]


def _cut(texture=None, crop: list = None):
    crop = crop or Window.size

    target_ratio = crop[0] / crop[1]
    texture_ratio = texture.width / texture.height

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

    texture = _cut(Image(source).texture, crop)
    makedirs(cache_folder, exist_ok=True)
    texture.save(path, flipped=False)
    Logger.debug("[KivyHome] Wallpaper: Stored the cropped wallpaper at %s", path)

    return texture
