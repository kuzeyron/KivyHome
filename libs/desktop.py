from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.carousel import Carousel
from .base import KivyHome

__all__ = ('Desktop', )

class Desktop(Carousel):
    initial = NumericProperty()
    smdirection = StringProperty('up')
    target = StringProperty('all_apps')
    scroll_distance = NumericProperty('100dp')
    ignore_perpendicular_swipes = BooleanProperty(True)

    def on__offset(self, *args):
        self._trigger_position_visible_slides()
        # if reached full offset, switch index to next or prev
        direction = self.direction[0]
        _offset = self._offset
        width = self.width
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

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        self.initial = touch.y

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        if all([self.collide_point(*touch.pos),
                self.initial > (self.height - (self.height / 2.5)),
                touch.dy > 0]):
            return KivyHome().change_direction(self.smdirection,
                                               self.target)
        return False
