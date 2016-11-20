import math
import timing


class ListChooser:
    """Chooses value from a list"""
    _choices = []
    _number_chooser = {}

    def __init__(self, choices):
        self._choices = choices
        self._number_chooser = NumberChooser(0, len(choices) - 1)

    def choose(self, position):
        choice = self._number_chooser.choose(position)
        return self._choices[choice]


class NumberChooser:
    """Chooses an integer between two values"""
    minimum = 0
    maximum = 0

    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def choose(self, position):
        return round(position * (self.maximum - self.minimum)) + self.minimum


class LengthChooser:
    """Chooses note lengths"""

    def __init__(self):
        self._lengths = [timing.note_time(1 / 16), timing.note_time(1 / 8), timing.note_time(1 / 4), timing.note_time(1 / 2)]
        self._list_chooser = ListChooser(self._lengths)

    def choose_length(self, position):
        return self._list_chooser.choose(position)


class PitchChooser:
    """Chooses MIDI pitches"""
    _scale_maj = [0, 2, 4, 5, 7, 9, 11]
    _scale_maj_penta = [0, 2, 4, 7, 9]
    _root = 0
    _list_chooser = ListChooser(_scale_maj_penta)

    def __init__(self, root):
        self._root = root

    def choose_pitch(self, position, octaves=1.0):
        scaled_position = position * octaves
        octave = math.floor(scaled_position)
        cycle_position = scaled_position - octave

        scale_pitch = self._list_chooser.choose(cycle_position)

        pitch = self._root + scale_pitch + octave * 12
        return pitch


class VelocityChooser:
    """Chooses MIDI velocities"""
    _number_chooser = NumberChooser(0, 127)

    def choose_velocity(self, position):
        return self._number_chooser.choose(position)