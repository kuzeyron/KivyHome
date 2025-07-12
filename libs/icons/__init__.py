from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (BooleanProperty, ListProperty, NumericProperty,
                             ObjectProperty, StringProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.utils import platform
from kivy.graphics import Color, Ellipse
from kivy.uix.progressbar import ProgressBar
from ..base import KivyHome
from ..utils import importer

__all__ = ('Applications', 'AppContainer', 'AppList', )

GetApps = importer(f'libs.icons.platforms.{platform}', 'GetPackages')
KV = '''
#:import platform kivy.utils.platform

<ProgressHolder>:
    auto_dismiss: False
    background_color: .2, .2, .5, 0
    canvas.before:
        Color:
            rgba: 0, 0, 0, self.opacity
        RoundedRectangle:
            size: self.size
            pos: self.pos

    CircularProgressBar:
        size_hint: .5, .5

<DesktopApplications>:
    orientation: 'bt-rl' if platform == 'android' else 'tb-lr'
    padding: dp(20), 0
    spacing: dp(10), dp(3)

<AppContainer>:
    size_hint_y: .99
    canvas.before:
        Color:
            rgba: 0, 0, 0, .3
        RoundedRectangle:
            pos: self.pos
            radius: (dp(10), )
            size: self.size
        Color:
            rgba: 1, 1, 1, .1
        SmoothLine:
            width: dp(1)
            rounded_rectangle: self.x, self.y, self.width, \
                self.height, dp(10)

    AppList:
        bar_width: dp(10)
        do_scroll_x: False
        BoxLayout:
            padding: 0, 0, 0, root.navigation_bar_height
            height: self.minimum_height
            size_hint_y: None
            Applications:
                height: self.minimum_height
                size_hint_y: None
                spacing: dp(20 if platform == 'android' else 35), dp(5)
'''


class CircularProgressBar(ProgressBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.thickness = dp(40)
        self.draw()

    def draw(self):
        max_size = min(self.size)
        
        with self.canvas:
            self.canvas.clear()

            Color(.26, .26, .26)
            Ellipse(pos=(self.center_x - max_size / 2, self.center_y - max_size / 2),
                    size=(max_size, max_size))

            Color(.2, .2, .5)
            Ellipse(pos=(self.center_x - max_size / 2, self.center_y - max_size / 2),
                    size=(max_size, max_size), angle_start=0, angle_end=(float(self.value_normalized * 360)))

            Color(0, 0, 0)
            inner_diameter = max_size - self.thickness
            Ellipse(pos=(self.center_x - inner_diameter / 2, self.center_y - inner_diameter / 2),
                    size=(inner_diameter, inner_diameter))

    def set_value(self, value):
        self.value = value + 1
        self.draw()


class ProgressHolder(ModalView):
    isbusy = BooleanProperty(None)
    opacity = NumericProperty(.6)

    def on_isbusy(self, _, busy):
        if busy:
            self.open()
        else:
            a = Animation(opacity=0, d=1)
            a.bind(on_complete=self.dismiss)
            a.start(self)


class Applications(GetApps, StackLayout):  # type: ignore
    isbusy = BooleanProperty(False)
    padding = ListProperty((dp(10), dp(10), dp(10), dp(20)))
    popup = ObjectProperty()

    def __init__(self, **kwargs):
        self.popup = ProgressHolder()
        super().__init__(**kwargs)


class AppList(ScrollView):
    __events__ = ('on_event', )
    direction = StringProperty('down')
    do_scroll_x = BooleanProperty(False)
    pressure = NumericProperty(3)
    target = StringProperty('main')

    def on_scroll_y(self, _, value):
        if any((
                self._viewport.height >= self.height and value >= self.pressure,
                value < -self.pressure and platform != 'android'
        )):
            # all, can scroll
            # all, revert direction on Linux when no room to scroll (fails in maximized window)
            self.dispatch('on_event')

    def on_event(self):
        KivyHome().change_direction(orientation=self.direction,
                                    target=self.target)


class AppContainer(BoxLayout):
    navigation_bar_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.home = KivyHome()
        self.navigation_bar_height = self.home.navigation_bar_height
        self.home.bind(navigation_bar_height=self.set_navigation_bar_height)

    def set_navigation_bar_height(self, _, height):
        self.navigation_bar_height = height


class DesktopApplications(StackLayout):
    def __init__(self, **kwargs):
        Builder.load_string(KV)
        super().__init__(**kwargs)
