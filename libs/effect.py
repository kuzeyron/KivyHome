from kivy.effects.dampedscroll import DampedScrollEffect
from kivy.properties import BooleanProperty
from kivy.utils import platform

from libs.base import KivyHome

class SwipeToHome(DampedScrollEffect):
    go_home = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._home_widget = KivyHome()

    def update_velocity(self, dt):
        if abs(self.velocity) <= self.min_velocity and self.overscroll == 0:
            self.velocity = 0
            # why does this need to be rounded? For now refactored it.
            if self.round_value:
                self.value = round(self.value)
            return

        total_force = self.velocity * self.friction * dt / self.std_dt
        if abs(self.overscroll) > self.min_overscroll:
            total_force += self.velocity * self.edge_damping
            total_force += self.overscroll * self.spring_constant
        else:
            self.overscroll = 0
            self.go_home = False

        stop_overscroll = ''
        if not self.is_manual:
            if self.overscroll > 0 and self.velocity < 0:
                stop_overscroll = 'max'
            elif self.overscroll < 0 and self.velocity > 0:
                stop_overscroll = 'min'

        self.velocity = self.velocity - total_force
        if not self.is_manual:
            self.apply_distance(self.velocity * dt)
            if stop_overscroll == 'min' and self.value > self.min:
                self.value = self.min
                self.velocity = 0
                return
            if stop_overscroll == 'max' and self.value < self.max:
                self.value = self.max
                self.velocity = 0
                return
        self.trigger_velocity_update()

    def on_overscroll(self, *args):
        overscroller = self.overscroll / float(self.target_widget.height)
        alpha_pressure = .8 if platform == 'android' else .6
        alpha = float(1. - abs(overscroller))

        self.target_widget.opacity = min(1, alpha)

        if alpha_pressure > alpha and overscroller < 0:
            self.go_home = True

        self.trigger_velocity_update()

    def on_go_home(self, _, value):
        if value:
            self._home_widget.change_direction(orientation='down',
                                               target='main')
