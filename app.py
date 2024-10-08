import streamlit as st
from scamp import *
from mingus.core import chords
import random as rand

# MIDI note mapping for base note (root)
note_to_midi = {'C': 60, 'C#': 61, 'Db': 61, 'D': 62, 'D#': 63, 'Eb': 63, 'E': 64,
                'Fb': 64, 'F': 65, 'F#': 66, 'Gb': 66, 'G': 67, 'G#': 68, 'Ab': 68, 'A': 69,
                'A#': 70, 'Bb': 70, 'B': 71, 'Cb': 71}

chord_type = [
        "major",  # Root, Major third, Perfect fifth
        "minor",  # Root, Minor third, Perfect fifth
        "major_seventh",  # Root, Major third, Perfect fifth, Major seventh
        "minor_seventh",  # Root, Minor third, Perfect fifth, Minor seventh
        "diminished",  # Root, Minor third, Diminished fifth
        "augmented",  # Root, Major third, Augmented fifth
        "diminished_seventh",  # Root, Minor third, Diminished fifth, Diminished seventh
        "dominant_seventh",  # Root, Major third, Perfect fifth, Minor seventh
        "major_ninth",  # Root, Major third, Perfect fifth, Major seventh, Major ninth
        "minor_ninth",  # Root, Minor third, Perfect fifth, Minor seventh, Major ninth
        "dominant_ninth",  # Root, Major third, Perfect fifth, Minor seventh, Major ninth
        "sus2",  # Root, Major second, Perfect fifth
        "sus4",  # Root, Perfect fourth, Perfect fifth
        "add9",  # Root, Major third, Perfect fifth, Major ninth
        "minor_add9",  # Root, Minor third, Perfect fifth, Major ninth
        "major_sixth",  # Root, Major third, Perfect fifth, Major sixth
        "minor_sixth",  # Root, Minor third, Perfect fifth, Major sixth
        "dominant_seventh_flat_five",  # Root, Major third, Diminished fifth, Minor seventh
        "dominant_seventh_sharp_nine",  # Root, Major third, Perfect fifth, Minor seventh, Augmented ninth
        "minor_seventh_flat_five",  # Root, Minor third, Diminished fifth, Minor seventh
        "sus2_seventh",  # Root, Major second, Perfect fifth, Minor seventh
        "sus4_seventh",  # Root, Perfect fourth, Perfect fifth, Minor seventh
]

# Function to get the semitone intervals for different chord types
def get_chord_intervals(chord_type):
    intervals = {
        "sus2":                         [0, 2, 7],
        "sus2_seventh":                 [0, 2, 7, 10],

        "diminished":                   [0, 3, 6],
        "diminished_seventh":           [0, 3, 6, 9],
        "minor_seventh_flat_five":      [0, 3, 6, 10],
        "minor":                        [0, 3, 7],
        "minor_sixth":                  [0, 3, 7, 9],
        "minor_seventh":                [0, 3, 7, 10],
        "minor_ninth":                  [0, 3, 7, 10, 14],
        "minor_add9":                   [0, 3, 7, 14],

        "dominant_seventh_flat_five":   [0, 4, 6, 10],  # Root, Major third, Diminished fifth, Minor seventh
        "dominant_seventh_sharp_nine":  [0, 4, 7, 10, 15],  # Root, Major third, Perfect fifth, Minor seventh, Augmented ninth
        "major":                        [0, 4, 7],  # Root, Major third, Perfect fifth
        "major_sixth":                  [0, 4, 7, 9],  # Root, Major third, Perfect fifth, Major sixth
        "dominant_seventh":             [0, 4, 7, 10],  # Root, Major third, Perfect fifth, Minor seventh
        "dominant_ninth":               [0, 4, 7, 10, 14],  # Root, Major third, Perfect fifth, Minor seventh, Major ninth
        "major_seventh":                [0, 4, 7, 11],  # Root, Major third, Perfect fifth, Major seventh
        "major_ninth":                  [0, 4, 7, 11, 14],  # Root, Major third, Perfect fifth, Major seventh, Major ninth
        "add9":                         [0, 4, 7, 14],  # Root, Major third, Perfect fifth, Major ninth
        "augmented":                    [0, 4, 8],  # Root, Major third, Augmented fifth

        "sus4":                         [0, 5, 7],  # Root, Perfect fourth, Perfect fifth
        "sus4_seventh":                 [0, 5, 7, 10],  # Root, Perfect fourth, Perfect fifth, Minor seventh

        # "twinkle":                      [0, 0, 7, 7, 9, 9, 7], # twinkle
    }
    return intervals.get(chord_type, [0])  # Default to root if chord type is not found

# Function to play a chord based on parameters
def play_piece(chord_name, chord_type, instrument, tempo, volume):
    # Log parameters
    print(f"Playing {chord_name} {chord_type} chord at tempo {tempo} BPM and volume {volume}")
    
    # Get the root note's MIDI number
    root_midi = note_to_midi[chord_name]
    
    # Get chord intervals based on chord type (major or minor)
    intervals = get_chord_intervals(chord_type)
    
    # Calculate the MIDI numbers for each note in the chord by adding intervals to the root
    midi_notes = [root_midi + interval for interval in intervals]

    # Play the chord note by note (ascending)
    for note in midi_notes:
        instrument.play_note(note, volume, 60/(2 * tempo))  # Convert tempo to note duration
    
    # Play the chord note by note (descending)
    for note in reversed(midi_notes):
        instrument.play_note(note, volume, 60/(2 * tempo))  # Convert tempo to note duration

    # Play the full chord simultaneously
    instrument.play_chord(midi_notes, volume, 60/tempo)  # Play the entire chord at once

# Start SCAMP session
s = Session()
# s.print_default_soundfont_presets()
piano = s.new_part("e.piano")

st.title("Chord Preference Test")
st.write("Select which chord you prefer.")

test = chord_type
rand.shuffle(test)
sample = []

while (len(test) > 1):
    sample = []
    for i in range(0, len(test), 2):
        if i == len(test) - 1:
            sample.append(test[i])
            break

        st.write(f"Playing chords: {test[i]} and {test[i+1]}")
        if st.button(f"Play {test[i]}"):
            play_piece("C", test[i], piano, 60, 1.0)
        if st.button(f"Play {test[i+1]}"):
            play_piece("C", test[i+1], piano, 60, 1.0)

        choice = st.radio("Which do you prefer?", [test[i], test[i+1]])
        sample.append(choice)

    st.write(f"Selected samples: {sample}")
    test = sample

st.success(f'Congrats, your favorite chord type seems to be {sample[0]}.')
s.wait_for_children_to_finish()

