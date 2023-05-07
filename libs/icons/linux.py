from functools import partial
from threading import Thread

from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image

from .appicons import AppIcon

__all__ = ('GetPackages', )

class GetPackages:
    def on_kv_post(self, *largs):
        Thread(target=self.ready, daemon=True).start()

    def ready(self):
        Clock.schedule_once(partial(self.on_busy, True), 0)

        for fpack in range(1, 11):
            Clock.schedule_once(partial(self.add_one,
                                        name=f'Fake App ({fpack})',
                                        package=f'org.test.fake{fpack}',
                                        path=f'assets/icons/{fpack}.png'), 0)

        Clock.schedule_once(partial(self.on_busy, False), 0)

    def add_one(self, *largs, **kwargs):
        app = App.get_running_app()
        kwargs['texture'] = Image(kwargs['path']).texture
        kwargs['arguments'] = kwargs
        self.add_widget(AppIcon(**kwargs))

        if kwargs['package'] in app.desktop_icons:
            app.root.ids.desk_apps.ids.favorite_apps.add_widget(AppIcon(**kwargs))

    def on_busy(self, status, *largs):
        self.popup.isbusy = status
