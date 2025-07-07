from kivy.config import Config; Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from functools import partial

from kivy.app import App
from kivy.clock import Clock
from libs.base import KivyHome
from libs.startup import Startup


class MyApp(App, Startup):
    def build(self):
        return KivyHome()

    def on_resume(self):
        Clock.schedule_once(partial(self.root.change_target, 'up', 'main'), 0)

        return True


if __name__ == '__main__':
    MyApp().run()
