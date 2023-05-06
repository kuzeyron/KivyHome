from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_string('''
<Controllers>:
    size_hint: .4, .05
    pos_hint: {'center_x': .5}
    canvas.before:
        Color:
            rgba: 0, 0, 0, 0.3
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [dp(10), ]
        Color:
            rgba: 0, 0, 0, .5
        BoxShadow:
            pos: self.pos
            size: self.size
            offset: 0, -10
            spread_radius: -dp(20), -dp(20)
            border_radius: [dp(30), ] * 4
            blur_radius: dp(50)
        Color:
            rgba: 1, 1, 1, .1
        SmoothLine:
            width: dp(1)
            rounded_rectangle: self.x, self.y, self.width, \
                self.height, dp(10)

    CheckBox:
        group: 'controls'
        on_active: app.change_target('right', 'main')
    CheckBox:
        group: 'controls'
        on_active: app.change_target('right', 'media')
    CheckBox:
        group: 'controls'
        on_active: app.change_target('right', 'other')

''')


class Controllers(BoxLayout):
    pass
