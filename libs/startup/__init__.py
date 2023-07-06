from kivy.utils import platform

from ..utils import importer

__all__ = ('Startup', )

Startup = importer(f'libs.startup.platforms.{platform}', 'Startup')
