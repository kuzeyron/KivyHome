from threading import Thread

from kivy.animation import Animation
from kivy.clock import mainthread
from kivy.graphics import Color, Ellipse
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.stacklayout import StackLayout
from kivy.utils import platform

from .appicons import AppIcon
from ..base import KivyHome

__all__ = ('Applications', 'AppContainer', 'AppList')

if platform == 'android':
    from .platforms.android import GetPackages
else:
    from .platforms.linux import GetPackages

Builder.load_string('''
#:import platform kivy.utils.platform
#:import SwipeToHome libs.effect.SwipeToHome

<ProgressHolder>:
    auto_dismiss: False
    background_color: .2, .2, .5, 0

    CircularProgressBar:
        size_hint: .6, .6

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
            rounded_rectangle: self.x, self.y, self.width, self.height, dp(10)

    ScrollView:
        effect_cls: SwipeToHome
        bar_width: dp(10)
        do_scroll_x: False

        Applications:
            padding: dp(10), dp(10), dp(10), root.navigation_bar_height + dp(20)
            height: self.minimum_height
            size_hint_y: None
            spacing: dp(20 if platform == 'android' else 35), dp(5)
''')


class CircularProgressBar(ProgressBar):
    __events__ = ('on_draw', )
    thickness = NumericProperty('40dp')

    def on_kv_post(self, _) -> None:
        self.dispatch('on_draw')

    def on_draw(self) -> None:
        max_size = min(self.size)

        with self.canvas:
            self.canvas.clear()

            Color(.26, .26, .26)
            Ellipse(pos=(self.center_x - max_size / 2, self.center_y - max_size / 2),
                    size=(max_size, max_size))

            Color(.2, .2, .5)
            Ellipse(pos=(self.center_x - max_size / 2, self.center_y - max_size / 2),
                    size=(max_size, max_size), angle_start=0, angle_end=(float(self.value_normalized * 360)))

            Color(0, 0, 0, .6)
            inner_diameter = max_size - self.thickness
            Ellipse(pos=(self.center_x - inner_diameter / 2, self.center_y - inner_diameter / 2),
                    size=(inner_diameter, inner_diameter))

    def set_value(self, value: int) -> None:
        self.value = value + 1
        self.dispatch('on_draw')


class ProgressHolder(ModalView):
    isbusy = BooleanProperty(None)

    def on_isbusy(self, _, busy: bool):
        if busy:
            self.open()
        else:
            a = Animation(opacity=0, d=1)
            a.bind(on_complete=self.dismiss)
            a.start(self)


class Applications(GetPackages, StackLayout):
    __events__ = ('on_busy', )
    isbusy = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popup = ProgressHolder()
        self._home_widget = KivyHome()

    def on_kv_post(self, _) -> None:
        Thread(target=self.find_applications, daemon=True).start()

    @mainthread
    def add_one(self, step: int, **kwargs) -> None:
        self.popup.children[0].set_value(step)

        if not kwargs['old']:
            kwargs['texture'].save(kwargs['path'], flipped=False)
        
        kwargs['arguments'] = kwargs

        if desktop_type :=  self._home_widget.desktop_icons.get(kwargs['package']):
            category_type = desktop_type['desktop_type']
            kwargs['desktop_type'] = category_type
            instance = self._home_widget.ids[category_type]
            instance.add_widget(AppIcon(**kwargs))

        self.add_widget(AppIcon(**kwargs))
 
    @mainthread
    def on_busy(self, status: bool) -> None:
        self.popup.children[0].max = self.amount_of_applications
        self.popup.isbusy = status


class AppContainer(BoxLayout):
    navigation_bar_height = NumericProperty()

    def on_kv_post(self, _) -> None:
        self._home_widget = KivyHome()
        self.navigation_bar_height = self._home_widget.navigation_bar_height
        self._home_widget.bind(navigation_bar_height=self.set_navigation_bar_height)

    def set_navigation_bar_height(self, _, height: float) -> None:
        self.navigation_bar_height = height


class DesktopApplications(StackLayout):
    pass
