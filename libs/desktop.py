from kivy.app import App
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.carousel import Carousel

__all__ = ('Desktop', )

class Desktop(Carousel):
    initial = NumericProperty()
    smdirection = StringProperty('up')
    target = StringProperty('all_apps')
    ignore_perpendicular_swipes = BooleanProperty(True)

    def on__offset(self, *args):
        self._trigger_position_visible_slides()
        # if reached full offset, switch index to next or prev
        direction = self.direction[0]
        _offset = self._offset
        width = self.width
        height = self.height
        index = self.index
        if self._skip_slide is not None or index is None:
            return

        # Move to next slide?
        if (direction == 'r' and _offset <= -width) or \
                (direction == 'l' and _offset >= width):
                    if self.next_slide:
                        self.index += 1

        # Move to previous slide?
        elif (direction == 'r' and _offset >= width) or \
            (direction == 'l' and _offset <= -width):
                if self.previous_slide:
                    self.index -= 1

        elif self._prev_equals_next:
            new_value = (_offset < 0) is (direction in 'r')
            if self._prioritize_next is not new_value:
                self._prioritize_next = new_value
                if new_value is (self._next is None):
                    self._prev, self._next = self._next, self._prev

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        self.initial = touch.y

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        if all([self.collide_point(*touch.pos),
                self.initial < touch.x,
                touch.dy > 0]):
            return App.get_running_app().change_target(self.smdirection,
                                                       self.target)
        return False
