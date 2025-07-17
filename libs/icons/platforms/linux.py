import time
from io import BytesIO
from os import makedirs
from os.path import getmtime, isfile, join
from shutil import rmtree

from android.storage import app_storage_path
from jnius import autoclass, cast

from kivy.core.image import Image
from kivy.logger import Logger

__all__ = ('GetPackages', )

class GetPackages:
    apps_path: str = '/usr/share/applications'

    def ready(self):
        self._home_widget = KivyHome()
        applications = sorted([x for x in listdir(self.apps_path) if x.endswith('.desktop')])
        self.amount_of_applications = len(applications)
        Clock.schedule_once(partial(self.on_busy, True), 0)

        for step, application in enumerate(applications, 1):
            with open(join(self.apps_path, application), encoding='utf-8') as file:
                for fileline in file:
                    if fileline.startswith('Icon='):
                        line = fileline[5:-1]
                        name = " ".join([nm.title() for nm in splitter('[.-]', line.split('.')[-1])])

                        if line.endswith('.png') and isfile(line):
                            icon_path = line
                        elif icon := glob(f"/usr/share/icons/*/128*/*/{line}.png"):
                            icon_path = icon[0]
                        else:
                            continue

                        Logger.debug('[KivyHome] Loading icon: %s', icon_path)
                        icon = Image(icon_path)
                        self.add_one(step, name=name, package=application, texture=icon, old=True)
