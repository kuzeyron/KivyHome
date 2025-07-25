from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout

from .applauncher import launch_app
from .buttonbehavior import LongPress

Builder.load_string('''
<AppIcon>:
    orientation: 'vertical'
    size: dp(63), dp(83)
    size_hint: None, None
    Widget:
        size: dp(63), dp(63)
        size_hint: None, None
        canvas.before:
            Color:
                rgba: 1, 1, 1, root.color_opacity
            RoundedRectangle:
                pos: self.x + dp(2), self.y + dp(2)
                radius: (dp(15), )
                size: self.width - dp(4), self.height - dp(4)
                texture: root.texture.texture
    Label:
        color: 1, 1, 1, .8
        font_size: dp(10)
        halign: 'center'
        height: dp(12)
        max_lines: 1
        shorten: True
        size: self.texture_size
        size_hint_y: None
        text: root.name
        text_size: root.width, None
''')


class AppIcon(LongPress, BoxLayout):
    arguments: dict = {}
    desktop_type = StringProperty('desktop_applications')
    listing: str = ''
    name = StringProperty()
    old = BooleanProperty()
    package = StringProperty()
    path = StringProperty()
    texture = ObjectProperty()

    def on_execution(self) -> None:
        launch_app(self.package)
