from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform

from libs.android_hide_system_bars import HideBars
from libs.wallpaper import wallpaper

if platform not in {'android', 'ios'}:
    from kivy.core.window import Window
    from kivy.metrics import dp
    Window.size = dp(400), dp(650)
    Logger.debug("Application is not Android.")

Builder.load_string('''
#:import Applications libs.icons.AppContainer
#:import DesktopApplications libs.icons.DesktopApplications
#:import Media libs.media.Media

<Basement>:
    padding: 0, app.cutout_height + dp(5), 0, 0
    orientation: 'vertical'
    canvas.before:
        Color:
            rgb: 1, 1, 1
        Rectangle:
            texture: app.bg
            size: self.size
            pos: self.pos
    
    BoxLayout:
        size_hint: .4, .05
        CheckBox:
            active: True
            group: 'controls'
            on_active: app.change_target('right', 'main')
        CheckBox:
            group: 'controls'
            on_active: app.change_target('right', 'media')
        CheckBox:
            group: 'controls'
            on_active: app.change_target('right', 'other')

    ScreenManager:
        id: sm

        Screen:
            name: 'main'
            BoxLayout:
                padding: 0, app.cutout_height + dp(5), 0, app.navbar_height + dp(5)
                DesktopApplications:
                    id: desk_apps
                    orientation: 'bt-rl'
                    padding: [dp(10)] * 2
                    spacing: [dp(10)] * 2

        Screen:
            name: 'media'
            on_leave: self.clear_widgets()
            on_pre_enter: self.add_widget(Media())

        Screen:
            name: 'other'
            
        Screen:
            name: 'all_apps'
            AppContainer:
''')


class Basement(BoxLayout):
    pass


class ProjectSimplifier(App, HideBars):
    bg = ObjectProperty(None, allownone=True)
    desktop_icons = ListProperty(['org.test.fake2', 'org.test.fake5', 'com.android.settings',
                                  'com.huawei.camera', 'in.krosbits.musicolet', 'org.kuzeyron.eyesight',
                                  'com.discord', 'com.ebay.mobile', 'com.github.android',
                                  'org.mozilla.firefox', ])

    def build(self):
        self.bg = wallpaper('assets/wallpapers/city.jpg')
        return Basement()

    def change_target(self, orientation, target, *largs):
        manager = self.root.ids.sm
        manager.transition.direction = orientation
        manager.current = target


if __name__ == '__main__':
    ProjectSimplifier().run()
