from kivy.lang import Builder
from kivy.properties import (BooleanProperty, DictProperty, ObjectProperty,
                             StringProperty)
from kivy.uix.boxlayout import BoxLayout

from .applauncher import launch_app
from .buttonbehavior import LongPress

Builder.load_string('''
<AppIcon>:
    orientation: 'vertical'
    size_hint: None, None
    size: dp(63), dp(83)
    Widget:
        size: dp(63), dp(63)
        size_hint: None, None
        canvas.before:
            Color:
                rgba: 1, 1, 1, root.color_opacity
            RoundedRectangle:
                pos: self.x + dp(2), self.y + dp(2)
                radius: (dp(15), )
                segments: 20
                size: self.width - dp(4), self.height - dp(4)
                texture: root.texture
    Label:
        color: 1, 1, 1, .8
        font_size: dp(9.5)
        outline_width: dp(1)
        size_hint_y: None
        height: dp(12)
        text: root.name
''')


class AppIcon(LongPress, BoxLayout):
    name = StringProperty()
    old = BooleanProperty()
    package = StringProperty()
    path = StringProperty()
    texture = ObjectProperty(None, allownone=True)
    listing = StringProperty()
    arguments = DictProperty()
    dtype = StringProperty('desk_favs')

    def on_execution(self, *largs):
        super().on_execution(*largs)
        launch_app(self.package)
