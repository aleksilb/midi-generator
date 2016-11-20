import math
import random


class TriangleMod:
    """Gives cyclic values of a triangle wave"""
    _cycle = None

    def __init__(self, cycle):
        self._cycle = cycle

    def value(self, time):
        cycle_pos = time % self._cycle
        adjust_pos = (cycle_pos - self._cycle / 2) / (self._cycle / 2)

        return 1 - abs(adjust_pos)


class SineMod:
    """Gives cyclic values of a sine wave"""
    _cycle = None

    def __init__(self, cycle):
        self._cycle = cycle

    def value(self, time):
        cycle_pos = time % self._cycle
        adjust_pos = (cycle_pos / self._cycle) * (math.pi * 2)

        value = (math.sin(adjust_pos) + 1) / 2
        return value


class RandMod:
    """Gives random values"""

    def value(self, time):
        return random.random()


class SampleHoldMod:
    """Takes modulation value and holds it for a given time"""
    hold_time = 0
    _held_values = {}

    def __init__(self, hold_time):
        self.hold_time = hold_time

    def value(self, time, value):
        hold_slot = math.floor(time / self.hold_time)
        if hold_slot in self._held_values:
            return self._held_values[hold_slot]
        else:
            self._held_values[hold_slot] = value
            return value

