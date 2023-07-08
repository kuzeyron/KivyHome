from functools import partial
from glob import glob
from os import listdir
from os.path import isfile, join
from re import split as splitter
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image

from ..appicons import AppIcon

__all__ = ('GetPackages', )

class GetPackages:
    def on_kv_post(self, *largs):
        Thread(target=self.ready, daemon=True).start()

    def ready(self):
        Clock.schedule_once(partial(self.on_busy, True), 0)
        apps_path = '/usr/share/applications'
        for file in sorted(listdir(apps_path)):
            if file.endswith('.desktop'):
                with open(join(apps_path, file), encoding='utf-8') as fl:
                    for ln in fl:
                        if ln.startswith('Icon='):
                            # Attempt on finding through .desktop
                            line = ln[5:].strip()
                            name = " ".join([nm.title() for nm in splitter('[.-]',
                                                    line.split('.')[-1])])
                            if isfile(line) and line.endswith('.png'):
                                Clock.schedule_once(partial(self.add_one,
                                                            name=name,
                                                            package=file,
                                                            path=line), 0)
                                break

                            # Try finding the icon from known areas
                            for icon in glob(f"/usr/share/icons/*/128*/*/{line}.png"):
                                Clock.schedule_once(partial(self.add_one,
                                                            name=name,
                                                            package=file,
                                                            path=icon), 0)
                                break


        Clock.schedule_once(partial(self.on_busy, False), 0)

    def add_one(self, *largs, **kwargs):
        _app = App.get_running_app()
        kwargs['texture'] = Image(kwargs['path'], mipmap=True).texture
        kwargs['arguments'] = kwargs

        if dtype :=  _app.desktop_icons.get(kwargs['package'], False):
            if dtype := dtype.get('dtype', kwargs.get('dtype', False)):
                kwargs['dtype'] = dtype
                instance = _app.root.ids[kwargs['dtype']]
                instance.add_widget(AppIcon(**kwargs))

        self.add_widget(AppIcon(**kwargs))

    def on_busy(self, status, *largs):
        self.popup.isbusy = status
