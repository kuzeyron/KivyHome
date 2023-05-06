from os import makedirs, stat
from os.path import basename, isfile, join

from kivy.core.image import Image
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.utils import platform

from libs.utils import importer

__all__ = ('wallpaper', )

if platform == 'android':
    app_storage_path = importer('android.storage', 'app_storage_path')
else:
    def app_storage_path():
        return ''

def _cut(texture=None, crop=None):
    """ Cropping mechanism thanks to Cheaterman """
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


def wallpaper(source=None, crop=None, mipmap=None):
    filesize = stat(source).st_size
    filename = f"{filesize};{basename(source)}"
    cache_folder = join(app_storage_path(), '.cache', 'wallpapers')
    makedirs(cache_folder, exist_ok=True)
    path = join(cache_folder, filename)
    mipmap = mipmap or False
        
    if isfile(path):
        texture = Image(path, mipmap=mipmap).texture
    else:
        texture = _cut(Image(source, mipmap=mipmap).texture)
        texture.save(path, flipped=False)

    return texture
