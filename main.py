from mido import Message, MidiFile, MidiTrack
import math
import random

def main():
    pitch_chooser = PitchChooser(60)
    octave_chooser = NumberChooser(1, 3)
    length_chooser = LengthChooser()
    velocity_chooser = VelocityChooser()
    pitch_mod = SineMod(1300)
    octave_mod = RandMod()
    octave_mod_snh = SampleHoldMod(note_time(1/4))
    #pitch_mod_1 = RandMod()
    #pitch_mod = SampleHoldMod(note_time(1/2))
    length_mod = TriangleMod(800)
    velocity_mod = SineMod(220)
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=12, time=0))

    time = 0
    bars = 4

    while time < note_time(4 * bars):
        len_mod_val = length_mod.value(time)
        note_length = length_chooser.choose_length(len_mod_val)

        #ptc_mod_val = pitch_mod.value(time, pitch_mod_1.value(time))
        ptc_mod_val = pitch_mod.value(time)
        oct_mod_val = octave_mod_snh.value(time, octave_mod.value(time))
        octave = octave_chooser.choose(oct_mod_val)
        print(oct_mod_val)
        print(octave)
        pitch = pitch_chooser.choose_pitch(ptc_mod_val, octave)

        vel_mod_val = velocity_mod.value(time)
        velocity = velocity_chooser.choose_velocity(vel_mod_val)

        track.append(Message('note_on', note=pitch, velocity=velocity, time=0))
        track.append(Message('note_off', note=pitch, velocity=velocity, time=note_length))
        time += note_length

    mid.save('new_song.mid')


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
