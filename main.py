from mido import Message, MidiFile, MidiTrack
import math


def main():
    pitch_chooser = PitchChooser(60)
    length_chooser = LengthChooser()
    velocity_chooser = VelocityChooser()
    pitch_lfo = SineLFO(1300)
    length_lfo = TriangleLFO(800)
    velocity_lfo = SineLFO(220)
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=12, time=0))

    time = 0

    while time < 32 * 120:
        len_lfo_val = length_lfo.get_value(time)
        note_length = length_chooser.choose_length(len_lfo_val)

        ptc_lfo_val = pitch_lfo.get_value(time)
        pitch = pitch_chooser.choose_pitch(ptc_lfo_val, 1.5)

        vel_lfo_val = velocity_lfo.get_value(time)
        velocity = velocity_chooser.choose_velocity(vel_lfo_val)

        track.append(Message('note_on', note=pitch, velocity=velocity, time=0))
        track.append(Message('note_off', note=pitch, velocity=velocity, time=note_length))
        time += note_length

    mid.save('new_song.mid')


class TriangleLFO:
    """Gives cyclic values of a triangle wave"""
    _cycle = None

    def __init__(self, cycle):
        self._cycle = cycle

    def get_value(self, time):
        cycle_pos = time % self._cycle
        adjust_pos = (cycle_pos - self._cycle / 2) / (self._cycle / 2)

        return 1 - abs(adjust_pos)


class SineLFO:
    """Gives cyclic values of a sine wave"""
    _cycle = None

    def __init__(self, cycle):
        self._cycle = cycle

    def get_value(self, time):
        cycle_pos = time % self._cycle
        adjust_pos = (cycle_pos / self._cycle) * (math.pi * 2)

        value = (math.sin(adjust_pos) + 1) / 2
        return value


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
        self._lengths = [note_time(1/16), note_time(1/8), note_time(1/4), note_time(1/2)]
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


def note_time(notes):
    _note_length = 480
    return round(notes * _note_length)

main()
