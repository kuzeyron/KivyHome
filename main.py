from kivy.utils import platform
from libs import KivyHome

if platform != 'android':
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

if __name__ == '__main__':
    KivyHome().run()
