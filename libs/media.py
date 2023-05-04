from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

Builder.load_file('libs/media.kv')


class Icon(Widget):
    icon = StringProperty()
    source = StringProperty()
    
    def on_icon(self, *largs):
        self.source = f"assets/media/{self.icon}.png"


class RegularButton(ButtonBehavior, Icon):
    def on_release(self, *largs):
        self.parent.access(self.icon)


class StickyButton(ToggleButtonBehavior, Icon):
    def on_release(self, *largs):
        self.parent.access(self.icon)


class Media(BoxLayout):
    address = StringProperty('http://192.168.3.123')
    port = NumericProperty(5555)

    def access(self, controller, *largs):
        UrlRequest(f"{self.address}:{self.port}/{controller}")
