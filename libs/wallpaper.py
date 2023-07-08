from os import makedirs, stat
from os.path import abspath, basename, dirname, isfile, join
from sys import argv

from kivy.core.image import Image
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.utils import platform

from libs.utils import importer

__author__ = 'cheaterman and kuzeyron'
__all__ = ('wallpaper', )

if platform == 'android':
    app_storage_path = importer('android.storage', 'app_storage_path')
else:
    def app_storage_path():
        return dirname(abspath(argv[0]))

def _cut(texture=None, crop=None):
    crop = crop or Window.size

    Logger.debug('Wallpaper: Cropping {texture.size=%s} to {crop=%s}', texture.size, crop)

    target_ratio = crop[0] / crop[1]
    target_width = target_ratio * texture.height

    if texture.width < target_width:
        return texture

    target_x = (texture.width - target_width) / 2

    return texture.get_region(x=target_x,
                              y=0,
                              width=target_width,
                              height=texture.height)


def wallpaper(source=None, crop=None, reset=None):
    filesize = stat(source).st_size
    filename = f"{filesize};{basename(source)}"
    cache_folder = join(app_storage_path(), '.cache', 'wallpapers')
    path = join(cache_folder, filename)
 
    if not reset and isfile(path):
        return Image(path).texture

    texture = Image(source).texture    
    
    if platform == 'android':
        texture = _cut(texture)    
        makedirs(cache_folder, exist_ok=True)
        texture.save(path, flipped=False)

    return texture
