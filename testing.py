from scamp import *
from mingus.core import chords
from util import *
import random as rand

# Start SCAMP session
s = Session()
# s.print_default_soundfont_presets()
piano = s.new_part("e.piano")

test = chord_type
rand.shuffle(test)
sample = []

while (len(test) > 1):
    sample = []
    for i in range(0, len(test), 2):
        if (i == len(test) - 1):
            sample.append(test[i])
            break
        choice = 'r'
        while (choice == 'r'):
            s.wait(1.0)
            play_piece("C", test[i], piano, 60, 1.0)
            s.wait(0.5)
            play_piece("C", test[i+1], piano, 60, 1.0)
            s.wait(1.0)
            choice = input("Type in [1] if you like the first, [2] for the second.\n[r] to repeat the piece: ")
        if (int(choice) == 1): 
            sample.append(test[i])
        else:
            sample.append(test[i+1])
    print(sample)
    test = sample

s.wait_for_children_to_finish()
print(f'Congrats, your favorite chord type seems to be {sample[0]}.')


