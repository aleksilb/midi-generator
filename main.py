from mido import Message, MidiFile, MidiTrack
import math


def main():
    pitch_chooser = PitchChooser(60)
    length_chooser = LengthChooser()
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    #scale = [0, 2, 4, 5, 7, 9, 11]
    scale = [0, 2, 4, 7, 9]
    lengths = [30, 60, 120, 240]

    track.append(Message('program_change', program=12, time=0))

    time = 0

    while time < 32 * 120:

        current_length = length_chooser.choose_length(triangle(time / 70, 10, 1))

        pitch = pitch_chooser.choose_pitch(math.sin(time / 300), 1.5)

        print(pitch)

        track.append(Message('note_on', note=pitch, velocity=64, time=0))
        track.append(Message('note_off', note=pitch, velocity=127, time=current_length))
        time += current_length

    mid.save('new_song.mid')


def triangle(position, length, maximum):
    in_position = (position % length - (length / 2)) / (length / 2)

    return round((1 - abs(in_position)) * maximum)


class Chooser:
    """Chooses value from a list"""
    _choices = []

    def choose(self, position):
        choice = math.floor(position * len(self._choices))
        return self._choices[choice]


class LengthChooser(Chooser):
    """Chooses note lengths"""
    _choices = [30, 60, 120, 240]

    def choose_length(self, position):
        return self.choose(position)


class PitchChooser(Chooser):
    """Chooses MIDI pitches"""
    _scale = [0, 2, 4, 7, 9]
    _root = 0

    def __init__(self, root):
        self._root = root

    @staticmethod
    def choose(position, choices):
        return math.floor(position * choices)

    def choose_pitch(self, position, octaves=1):
        scale_selection = self.choose(position * octaves, len(self._scale))
        octave = math.floor(scale_selection / len(self._scale))
        scale_selection %= len(self._scale)

        pitch = self._root + self._scale[scale_selection] + octave * 12
        return pitch


main()
