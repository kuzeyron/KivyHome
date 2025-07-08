from kivy.app import App
from kivy.clock import Clock
from libs.base import KivyHome


class MyApp(App):
    def build(self):
        return KivyHome()

    def on_resume(self):
        Clock.schedule_once(self.root.change_direction, 0)

        return True


if __name__ == '__main__':
    MyApp().run()
