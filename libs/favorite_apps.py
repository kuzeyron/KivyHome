import json
import sys
from os import makedirs
from os.path import dirname, exists, join

from kivy.utils import platform

from libs.utils import importer

__all__ = ('get_default_path', 'get_default_file', 'write_to_file',
           'reset', 'file_exists', 'retrieve_favorite_apps',
           'store_favorite_apps')

def get_default_path():
    if platform == 'android':
        return importer('android.storage', 'app_storage_path')()

    return dirname(sys.argv[0])


def get_default_file():
    default_folder = join(get_default_path(), '.cache', 'data')
    makedirs(default_folder, exist_ok=True)

    return join(default_folder, 'favorite-apps.json')


def write_to_file(file, config):
    with open(file, 'w', encoding='utf-8') as s:
        s.write(json.dumps(config, indent=4, sort_keys=True))
    return config


def reset(file=None): 
    return write_to_file(file, [])


def file_exists(file=None):
    if exists(file):
        with open(file, encoding='utf-8') as s:
            return json.load(s)

    return reset(file)


def retrieve_favorite_apps(file=None):
    return file_exists(file or get_default_file())


def store_favorite_apps(file=None, config=None):
    if isinstance(config, (list, set, tuple)):
        return write_to_file(file or get_default_file(), config)

    raise Exception("We only support lists, sets and tuples")
