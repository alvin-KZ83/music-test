const chordTypes = [
    "major",  // Root, Major third, Perfect fifth
        "minor",  // Root, Minor third, Perfect fifth
        "major_seventh",  // Root, Major third, Perfect fifth, Major seventh
        "minor_seventh",  // Root, Minor third, Perfect fifth, Minor seventh
        "diminished",  // Root, Minor third, Diminished fifth
        "augmented",  // Root, Major third, Augmented fifth
        "diminished_seventh",  // Root, Minor third, Diminished fifth, Diminished seventh
        "dominant_seventh",  // Root, Major third, Perfect fifth, Minor seventh
        "major_ninth",  // Root, Major third, Perfect fifth, Major seventh, Major ninth
        "minor_ninth",  // Root, Minor third, Perfect fifth, Minor seventh, Major ninth
        "dominant_ninth",  // Root, Major third, Perfect fifth, Minor seventh, Major ninth
        "sus2",  // Root, Major second, Perfect fifth
        "sus4",  // Root, Perfect fourth, Perfect fifth
        "add9",  // Root, Major third, Perfect fifth, Major ninth
        "minor_add9",  // Root, Minor third, Perfect fifth, Major ninth
        "major_sixth",  // Root, Major third, Perfect fifth, Major sixth
        "minor_sixth",  // Root, Minor third, Perfect fifth, Major sixth
        "dominant_seventh_flat_five",  // Root, Major third, Diminished fifth, Minor seventh
        "dominant_seventh_sharp_nine",  // Root, Major third, Perfect fifth, Minor seventh, Augmented ninth
        "minor_seventh_flat_five",  // Root, Minor third, Diminished fifth, Minor seventh
        "sus2_seventh",  // Root, Major second, Perfect fifth, Minor seventh
        "sus4_seventh",  // Root, Perfect fourth, Perfect fifth, Minor seventh
];

let testChords = [...chordTypes];
let sample = [];

// Create a synth using Tone.js
const synth = new Tone.PolySynth(Tone.Synth).toDestination();

// MIDI note mapping for root note (C)
const noteToMidi = { 'C': 60, 'C#': 61, 'D': 62, 'D#': 63, 'E': 64, 'F': 65, 'F#': 66, 'G': 67, 'G#': 68, 'A': 69, 'A#': 70, 'B': 71 };

// Chord intervals for different types
const chordIntervals = {
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

    "dominant_seventh_flat_five":   [0, 4, 6, 10],
    "dominant_seventh_sharp_nine":  [0, 4, 7, 10, 15],
    "major":                        [0, 4, 7],
    "major_sixth":                  [0, 4, 7, 9],
    "dominant_seventh":             [0, 4, 7, 10],
    "dominant_ninth":               [0, 4, 7, 10, 14],
    "major_seventh":                [0, 4, 7, 11],
    "major_ninth":                  [0, 4, 7, 11, 14],
    "add9":                         [0, 4, 7, 14],
    "augmented":                    [0, 4, 8],

    "sus4":                         [0, 5, 7],
    "sus4_seventh":                 [0, 5, 7, 10],
};

// Function to play a chord
function playChord(root, chordType) {
    const rootMidi = noteToMidi[root];
    const intervals = chordIntervals[chordType];
    const chordNotes = intervals.map(interval => Tone.Frequency(rootMidi + interval, "midi").toNote());
    
    // Play the chord in ascending order
    chordNotes.forEach((note, i) => {
        synth.triggerAttackRelease(note, "8n", Tone.now() + i * 0.5);
    });
    
    // Then play the full chord together
    synth.triggerAttackRelease(chordNotes, "2n", Tone.now() + chordNotes.length * 0.5);
}

let currentPair = [];

// Play Chord 1
document.getElementById('playChord1').addEventListener('click', function() {
    if (currentPair.length === 0) {
        if (testChords.length >= 2) {
            currentPair = testChords.splice(0, 2);
        } else {
            nextRound();
        }
        updateButtonText();
    }
    playChord("C", currentPair[0]);
});

// Play Chord 2
document.getElementById('playChord2').addEventListener('click', function() {
    if (currentPair.length === 0) {
        if (testChords.length >= 2) {
            currentPair = testChords.splice(0, 2);
        } else {
            nextRound();
        }
        updateButtonText();
    }
    if (currentPair[1]) {
        playChord("C", currentPair[1]);
    }
});

// Update button text based on the current pair of chords
function updateButtonText() {
    document.getElementById('playChord1').innerText = currentPair[0] ? 'Play ' + currentPair[0] : 'Play Chord 1';
    document.getElementById('playChord2').innerText = currentPair[1] ? 'Play ' + currentPair[1] : 'Play Chord 2';
}

// Select Chord 1 as preferred
document.getElementById('selectChord1').addEventListener('click', function() {
    if (currentPair[0]) {
        sample.push(currentPair[0]);
    }
    nextRound();
});

// Select Chord 2 as preferred
document.getElementById('selectChord2').addEventListener('click', function() {
    if (currentPair[1]) {
        sample.push(currentPair[1]);
    }
    nextRound();
});

// Move to the next round of selection
function nextRound() {
    if (testChords.length > 1) {
        currentPair = testChords.splice(0, 2);
        updateButtonText();
        document.getElementById('result').innerText = "Next round starting...";
    } else if (testChords.length === 1) {
        sample.push(testChords[0]);
        resetForNextRound();
    } else {
        if (sample.length > 1) {
            resetForNextRound();
        } else {
            showCongratsPage(sample[0]);
        }
    }
}

// Reset for the next round
function resetForNextRound() {
    if (sample.length >= 2) {
        testChords = sample.slice();
        sample = [];
        currentPair = testChords.splice(0, 2);
        updateButtonText();
        document.getElementById('result').innerText = "Next round starting...";
    } else if (sample.length === 1) {
        // Redirect to congrats.html and pass the favorite chord as a URL parameter
        showCongratsPage(sample[0]); // Show the congrats page dynamically
    }
}

// Function to show congrats message
function showCongratsPage(favoriteChord) {
    // Hide the current content
    document.body.innerHTML = '';  // Clear the page
    
    // Create a new "Congrats" message
    const congratsDiv = document.createElement('div');
    congratsDiv.style.textAlign = 'center';
    congratsDiv.style.marginTop = '50px';
    
    const congratsHeading = document.createElement('h1');
    congratsHeading.innerText = 'Congratulations!';
    
    const congratsMessage = document.createElement('p');
    congratsMessage.innerText = `Your favorite chord type is: ${favoriteChord}.`;
    
    congratsDiv.appendChild(congratsHeading);
    congratsDiv.appendChild(congratsMessage);
    
    document.body.appendChild(congratsDiv);
}
