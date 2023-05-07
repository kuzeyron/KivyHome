from threading import Thread
from time import sleep

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ColorProperty, DictProperty,
                             NumericProperty, ObjectProperty, StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView

from libs.android_vibrator import vibrate

__all__ = ('LongPress', )

Builder.load_string('''
<AppMenuButton>:
    on_release: self.parent.parent.dismiss()
    font_size: dp(10)
    canvas.before:
        Color:
            rgba: (.3, .2, .3, .7) if self.state == 'down' else (.4, .3, .4, .7)
        Rectangle:
            size: self.size
            pos: self.pos

<AppMenu>:
    id: test
    size_hint: None, None
    size: dp(200), dp(200)
    background_color: .4, .3, .4, .7
    canvas.before:
        Clear
        Color:
            rgb: 0, 0, 0
        BoxShadow:
            pos: self.pos
            size: self.size
            offset: 0, 0
            spread_radius: -20, -20
            border_radius: 0, 0, 0, 0
            blur_radius: 50

    BoxLayout:
        orientation: 'vertical'

        AppMenuButton:
            text: f'Kill service for {root.app_name}'
        AppMenuButton:
            text: 'Add to home'
            on_release: self.add(root.package)
        AppMenuButton:
            text: 'Remove from home'
            on_release: self.remove(root.package)

''')

class AppMenuButton(ButtonBehavior, Label):
    def add(self, package):
        _app = App.get_running_app()

        if package not in _app.desktop_icons:
            _app.desktop_icons.append(package)
            fav = _app.root.ids.desk_apps.ids.favorite_apps
            fav.add_widget(Factory.AppIcon(**self.parent.parent.arguments))

    def remove(self, package):
        _app = App.get_running_app()
        _app.desktop_icons.remove(package)


class AppMenu(ModalView):
    package = StringProperty()
    app_name = StringProperty()
    caller = ObjectProperty(None, allownone=True)
    arguments = DictProperty()


class LongPress(ButtonBehavior):
    __events__ = ('on_execution', 'on_menu', 'on_trigger', )
    _vib = ObjectProperty(None, allownone=True)
    always_release = BooleanProperty(True)
    background_color = ColorProperty((.3, .2, .3, .7))
    long_tick = NumericProperty(1)
    count = NumericProperty(0)
    isfree = BooleanProperty(True)
    arguments = DictProperty()

    def on_state(self, instance, state):
        if state == 'down':
            self.background_color = (.4, .3, .4, .7)
            self.isfree = True
            self._clock = Clock.schedule_once(self.stop_counting, self.long_tick)
            Thread(target=self.start_counting, daemon=True).start()
        else:
            self.background_color = (.3, .2, .3, .7)
            self._clock.cancel()
            self.isfree = False

    def stop_counting(self, *largs):
        self.isfree = False

    def start_counting(self):
        while self.state == 'down' and self.isfree:
            self.count += .02
            sleep(.05)

        self.dispatch('on_trigger')

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        self.isfree = False
        self.count = 0

    @mainthread
    def on_trigger(self, *largs):
        if .2 > self.count > .02:
            self.dispatch('on_execution')
            self._vib = vibrate(.05)
        elif self.count > .3:
            self.dispatch('on_menu')
            self._vib = vibrate(.05)

    def on_execution(self, *largs):
        self.count = 0

    def on_menu(self, *largs):
        menu = AppMenu()
        menu.package = self.package
        menu.app_name = self.name
        menu.caller = self
        menu.arguments = self.arguments
        menu.open()
        self.count = 0

    def on_release(self, *largs):
        if self._vib is not None:
            self._vib.cancel()
