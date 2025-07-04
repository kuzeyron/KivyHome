from threading import Thread
from time import sleep

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, DictProperty, NumericProperty,
                             ObjectProperty, StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from libs.menu import ModalView
from libs.vibrator import vibrate

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

    def add(self, package):
        _app = App.get_running_app()

        if package not in _app.desktop_icons:
            collection = self.parent.parent.arguments
            collection.update(dict(dtype=self.dtype))
            _app.desktop_icons.update({package: collection})
            instance = _app.root.ids[self.dtype]
            instance.add_widget(Factory.AppIcon(**collection))

    def remove(self, package):
        _app = App.get_running_app()

        if dtype :=  _app.desktop_icons.get(package, False):
            if dtype := dtype.get('dtype', self.dtype):
                del _app.desktop_icons[package]
                instance = _app.root.ids[dtype]
                for child in instance.children:
                    if child.package == package:
                        instance.remove_widget(child)


class AppMenu(ModalView):
    package = StringProperty()
    app_name = StringProperty()
    caller = ObjectProperty(None, allownone=True)
    arguments = DictProperty()


class LongPress(ButtonBehavior):
    __events__ = ('on_execution', 'on_menu', 'on_trigger', )
    _vib = ObjectProperty(None, allownone=True)
    always_release = BooleanProperty(True)
    color_opacity = NumericProperty(1.)
    long_tick = NumericProperty(1)
    count = NumericProperty(0)
    isfree = BooleanProperty(True)
    arguments = DictProperty()

    def on_state(self, instance, state):
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

    def stop_counting(self, *largs):
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
    def on_trigger(self, *largs):
        if .01 < self.count < .1:
            self.dispatch('on_execution')
            self._vib = vibrate(.05)
        elif self.count > .1:
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
        menu.pos = self.last_touch.pos
        menu.parent_size = self.parent.size
        menu.open()
        self.count = 0

    def on_release(self, *largs):
        if self._vib is not None:
            self._vib.cancel()
