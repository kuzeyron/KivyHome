from threading import Thread
from time import sleep

from kivy.clock import Clock, mainthread
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, DictProperty, NumericProperty,
                             StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label

from ..base import KivyHome
from ..menu import ModalView
from ..vibrator import vibrate

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
    background_color: 0, 0, 0, 0
    overlay_color: 0, 0, 0, 0
    canvas:
        Clear
        Color:
            rgba: 0, 0, 0, 1
        BoxShadow:
            pos: self.pos
            size: self.size
            offset: 0, 0
            spread_radius: -10, -10
            border_radius: dp(10), dp(10), dp(10), dp(10)
            blur_radius: 50
        Color:
            rgba: 0, 0, 0, 1
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        pos: root.pos
        orientation: 'vertical'

        AppMenuButton:
            text: f'Kill service for {root.app_name}'
        AppMenuButton:
            text: 'Add to home'
            on_release: self.add(root.package)
        AppMenuButton:
            text: 'Add to drawyer'
            on_release:
                self.dtype = 'desk_favs'
                self.add(root.package)
        AppMenuButton:
            text: 'Remove from home'
            on_release: self.remove(root.package)

''')

class AppMenuButton(ButtonBehavior, Label):
    dtype = StringProperty('desk_apps')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._app = KivyHome()

    def add(self, package):
        if package not in self._app.desktop_icons:
            collection = self.parent.parent.arguments
            collection.update(dict(dtype=self.dtype))
            self._app.desktop_icons.update({package: collection})
            instance = self._app.ids[self.dtype]
            instance.add_widget(Factory.AppIcon(**collection))

    def remove(self, package):
        if dtype :=  self._app.desktop_icons.get(package, False):
            if dtype := dtype.get('dtype', self.dtype):
                del self._app.desktop_icons[package]
                instance = self._app.ids[dtype]
                for child in instance.children:
                    if child.package == package:
                        instance.remove_widget(child)


class AppMenu(ModalView):
    package: str = ''
    app_name = StringProperty()
    caller = None
    arguments: dict = {}


class LongPress(ButtonBehavior):
    __events__ = ('on_execution', 'on_menu', 'on_trigger')
    _vib = None
    always_release = BooleanProperty(True)
    arguments = DictProperty()
    color_opacity = NumericProperty(1.)
    count: int = 0
    isfree: bool = True
    long_tick: float = 1.

    def on_state(self, _, state):
        touch = self.last_touch.button
        if state == 'down' and touch in {'left', None}:
            self.color_opacity = .5
            self.isfree = True
            self._clock = Clock.schedule_once(self.stop_counting, self.long_tick)
            Thread(target=self.start_counting, daemon=True).start()
        elif state == 'down' and touch == 'right':
            self._clock = Clock.schedule_once(self.on_menu, 0)
        else:
            self.color_opacity = 1
            self._clock.cancel()
            self.isfree = False

    def stop_counting(self, _=None, value=None):
        self.isfree = False

    def start_counting(self):
        while self.state == 'down' and self.isfree:
            self.count += .02
            sleep(.05)

        self.dispatch('on_trigger')

    def on_touch_move(self, touch):
        self.isfree = False
        self.count = 0
        super().on_touch_move(touch)

    @mainthread
    def on_trigger(self):
        if .01 < self.count < .1:
            self.dispatch('on_execution')
            self._vib = vibrate(.05)
        elif self.count > .1:
            self.dispatch('on_menu')
            self._vib = vibrate(.05)

    def on_execution(self, *largs):
        self.count = 0

    def on_menu(self):
        menu = AppMenu()
        menu.package = self.package
        menu.app_name = self.name
        menu.caller = self
        menu.arguments = self.arguments
        menu.pos = self.last_touch.pos
        menu.parent_size = self.parent.size
        menu.open()
        self.count = 0

    def on_release(self):
        if self._vib is not None:
            self._vib.cancel()
