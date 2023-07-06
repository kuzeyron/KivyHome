from kivy.animation import Animation
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (BooleanProperty, ListProperty, NumericProperty,
                             ObjectProperty, StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.utils import platform

from .launchapps import launch_app
from ..utils import importer

__all__ = ('Applications', 'AppContainer', 'AppList', )

GetApps = importer(f'libs.icons.platforms.{platform}', 'GetPackages')
Builder.load_string('''
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

    Image:
        size_hint: None, None
        source: 'assets/images/loading.gif'
        anim_delay: 1/20

<DesktopApplications>:
    orientation: 'bt-rl' if platform == 'android' else 'tb-lr'
    padding: dp(10), 0
    spacing: dp(10), dp(3)

<AppContainer>:
    padding: 0, dp(10), 0, app.navbar_height or dp(10)
    canvas.before:
        Color:
            rgba: 0, 0, 0, .3
        RoundedRectangle:
            pos: self.pos
            radius: [dp(15), ]
            size: self.size

    AppList:
        bar_width: dp(3)
        do_scroll_x: False
        BoxLayout:
            height: self.minimum_height
            padding: [dp(5), ] * 4
            size_hint_y: None
            Applications:
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(0 if platform == 'android' else 20), \
                         dp(0 if platform == 'android' else 10)
''')

class ProgressHolder(ModalView):
    isbusy = BooleanProperty(None)
    opacity = NumericProperty(.6)

    def on_isbusy(self, *largs):
        if self.isbusy:
            self.open()
        else:
            a = Animation(opacity=0, d=1)
            a.bind(on_complete=self.dismiss)
            a.start(self)


class Applications(GetApps, StackLayout):  # type: ignore
    isbusy = BooleanProperty(False)
    padding = ListProperty([dp(10), ] * 4)
    popup = ObjectProperty()
    spacing = ListProperty([dp(10), ] * 2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popup = ProgressHolder()


class AppList(ScrollView):
    __events__ = ('on_event', )
    direction = StringProperty('down')
    scroll_distance = NumericProperty('40dp')
    scroll_timeout = NumericProperty(350)
    target = StringProperty('main')

    def on_scroll_y(self, *largs):
        if self.scroll_y > 1.22:
            self.dispatch('on_event')

    def on_event(self, *largs):
        App.get_running_app().change_target(self.direction,
                                            self.target)


class AppContainer(BoxLayout):
    pass


class DesktopApplications(StackLayout):
    pass
