from functools import partial
from glob import glob
from os import listdir
from os.path import isfile, join
from re import split as splitter
from threading import Thread
from time import sleep
from kivy.clock import Clock, mainthread
from kivy.core.image import Image

from ..appicons import AppIcon
from libs.base import KivyHome

__all__ = ('GetPackages', )

class GetPackages:
    def on_kv_post(self, _):
        Thread(target=self.ready, daemon=True).start()

    def ready(self):
        apps_path = '/usr/share/applications'
        self._home = KivyHome()
        applications = sorted([x for x in listdir(apps_path)
                               if x.endswith('.desktop')])
        self.amount_of_applications = len(applications)
        Clock.schedule_once(partial(self.on_busy, True), 0)
        for step, app in enumerate(applications, 1):
            with open(join(apps_path, app), encoding='utf-8') as fl:
                for ln in fl:
                    if ln.startswith('Icon='):
                        # Attempt on finding through .desktop files
                        line = ln[5:].strip()
                        name = " ".join([nm.title() for nm in splitter('[.-]',
                                                line.split('.')[-1])])

                        if line.endswith('.png') and isfile(line):
                            self.add_one(step, name=name, package=app, path=line)
                            break

                        # Try finding the icon from known areas
                        for icon in glob(f"/usr/share/icons/*/128*/*/{line}.png"):
                            self.add_one(step, name=name, package=app, path=icon)
                            break

        Clock.schedule_once(partial(self.on_busy, False), 1)

    @mainthread
    def add_one(self, step, **kwargs):
        self.popup.children[0].set_value(step)
        kwargs['texture'] = Image(kwargs['path'], mipmap=True)
        kwargs['arguments'] = kwargs

        if dtype :=  self._home.desktop_icons.get(kwargs['package'], {}).get('dtype'):
            kwargs['dtype'] = dtype
            instance = self._home.ids[kwargs['dtype']]
            instance.add_widget(AppIcon(**kwargs))

        self.add_widget(AppIcon(**kwargs))

    def on_busy(self, status, _):
        self.popup.children[0].max = self.amount_of_applications
        self.popup.isbusy = status
