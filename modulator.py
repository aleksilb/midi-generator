import math
import random


class CombinedMod:
    """Combines multiple modulators with given weights"""
    _modulators = []
    _weights = []
    _total_weight = 0

    def __init__(self, modulators, weights):
        self._modulators = modulators
        self._weights = weights
        for weight in weights:
            self._total_weight += weight

    def value(self, time):
        value = 0
        for index, modulator in enumerate(self._modulators):
            weight = self._weights[index] / self._total_weight
            value += weight * modulator.value(time)
        return value


class ValueMod:
    """Takes value of one modulator and modulates it with another"""
    _modulator = None
    _modulated = None

    def __init__(self, modulator, modulated):
        self._modulator = modulator
        self._modulated = modulated

    def value(self, time):
        orig_value = self._modulated.value(time)
        return self._modulator.value(time, orig_value)


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

    @staticmethod
    def value(time):
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


class InvertMod:
    """Takes modulation value and inverts it"""

    @staticmethod
    def value(time, value):
        return 1 - value
