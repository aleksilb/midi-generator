from mido import Message, MidiFile, MidiTrack
import math


def main():
    pitch_chooser = PitchChooser(60)
    length_chooser = LengthChooser()
    velocity_chooser = VelocityChooser()
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=12, time=0))

    time = 0

    while time < 32 * 120:
        current_length = length_chooser.choose_length(triangle(time / 70, 10, 1))
        pitch = pitch_chooser.choose_pitch(math.sin(time / 300), 1.5)
        velocity = velocity_chooser.choose_velocity(math.sin(time / 10))

        track.append(Message('note_on', note=pitch, velocity=velocity, time=0))
        track.append(Message('note_off', note=pitch, velocity=velocity, time=current_length))
        time += current_length

    mid.save('new_song.mid')


def triangle(position, length, maximum):
    in_position = (position % length - (length / 2)) / (length / 2)

    return round((1 - abs(in_position)) * maximum)


class ListChooser:
    """Chooses value from a list"""
    _choices = []
    _number_chooser = {}

    def __init__(self, choices):
        self._choices = choices
        self._number_chooser = NumberChooser(0, len(choices))

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
        return math.floor(position * (self.maximum - self.minimum)) + self.minimum


class LengthChooser:
    """Chooses note lengths"""
    _lengths = [30, 60, 120, 240]
    _list_chooser = ListChooser(_lengths)

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

    def choose_pitch(self, position, octaves=1):
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

main()
