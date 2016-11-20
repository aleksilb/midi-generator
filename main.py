from mido import Message, MidiFile, MidiTrack
import chooser
import timing
import modulator


def main():
    pitch_chooser = chooser.PitchChooser(60)
    octave_chooser = chooser.NumberChooser(1, 3)
    length_chooser = chooser.LengthChooser()
    velocity_chooser = chooser.VelocityChooser()
    pitch_mod_1 = modulator.SineMod(800)
    pitch_mod_2 = modulator.SineMod(2200)
    pitch_mod = modulator.CombinedMod([pitch_mod_1, pitch_mod_2], [1, 1])
    octave_mod_rnd = modulator.RandMod()
    octave_mod_snh = modulator.SampleHoldMod(timing.note_time(1/4))
    octave_mod = modulator.ValueMod(octave_mod_snh, octave_mod_rnd)
    #pitch_mod_1 = RandMod()
    #pitch_mod = SampleHoldMod(note_time(1/2))
    length_mod = modulator.TriangleMod(800)
    velocity_mod = modulator.SineMod(220)
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=12, time=0))

    time = 0
    bars = 4

    while time < timing.note_time(4 * bars):
        len_mod_val = length_mod.value(time)
        note_length = length_chooser.choose_length(len_mod_val)

        #ptc_mod_val = pitch_mod.value(time, pitch_mod_1.value(time))
        ptc_mod_val = pitch_mod.value(time)
        #oct_mod_val = octave_mod.value(time)
        #octave = octave_chooser.choose(oct_mod_val)
        octave = 3
        pitch = pitch_chooser.choose_pitch(ptc_mod_val, octave)

        vel_mod_val = velocity_mod.value(time)
        velocity = velocity_chooser.choose_velocity(vel_mod_val)

        track.append(Message('note_on', note=pitch, velocity=velocity, time=0))
        track.append(Message('note_off', note=pitch, velocity=velocity, time=note_length))
        time += note_length

    mid.save('new_song.mid')


main()
