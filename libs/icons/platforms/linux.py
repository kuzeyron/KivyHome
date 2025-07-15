from functools import partial
from glob import glob
from os import listdir
from os.path import isfile, join
from re import split as splitter
from threading import Thread

from kivy.clock import Clock, mainthread
from kivy.core.image import Image
from kivy.logger import Logger

from ..appicons import AppIcon
from libs.base import KivyHome

__all__ = ('GetPackages', )

class GetPackages:
    apps_path: str = '/usr/share/applications'

    def on_kv_post(self, _):
        Thread(target=self.ready, daemon=True).start()

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
                            Logger.debug('[KivyHome] Loading icon: %s', line)
                            self.add_one(step, name=name, package=application, path=line)
                        elif icon := glob(f"/usr/share/icons/*/128*/*/{line}.png"):
                            Logger.debug('[KivyHome] Loading icon: %s', icon[0])
                            self.add_one(step, name=name, package=application, path=icon[0])

                        break

        Clock.schedule_once(partial(self.on_busy, False), 0)

    @mainthread
    def add_one(self, step, **kwargs):
        self.popup.children[0].set_value(step)
        kwargs['texture'] = Image(kwargs['path'], mipmap=True)
        kwargs['arguments'] = kwargs

        if dtype :=  self._home_widget.desktop_icons.get(kwargs['package'], {}).get('dtype'):
            kwargs['dtype'] = dtype
            instance = self._home_widget.ids[kwargs['dtype']]
            instance.add_widget(AppIcon(**kwargs))

        self.add_widget(AppIcon(**kwargs))

    def on_busy(self, status, _):
        self.popup.children[0].max = self.amount_of_applications
        self.popup.isbusy = status
