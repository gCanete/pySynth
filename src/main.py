from pyo import *
import keyboard

# Frequencies https://homes.luddy.indiana.edu/donbyrd/Teach/MusicalPitchesTable.htm

# # Start the audio server
s = Server().boot()
s.start()

# Create a dictionary to keep track of active notes
active_notes = {}

# Mapping keys to frequencies (for example)
key_to_freq = {
    'a': 261.63,   # C4
    'w': 277.18,   # C#4/Db4
    's': 293.66,   # D4
    'e': 311.13,   # D#4/Eb4
    'd': 329.63,   # E4
    'f': 349.23,   # F4
    't': 369.99,   # F#4/Gb4
    'g': 392.00,   # G4
    'y': 415.30,   # G#4/Ab4
    'h': 440.00,   # A4
    'u': 466.16,   # A#4/Bb4
    'j': 493.88,   # B4
    'k': 523.25    # C5
}

def sound(freq, mode):
    if mode == 1:
        # Simple Sine wave
        return Sine(freq=freq, mul=0.2)
    elif mode == 2:
        # Sawtooth wave
        return SuperSaw(freq=freq, mul=0.2)
    elif mode == 3:
        # Square wave
        return Sine(freq, mul=0.2) + Sine(3*freq)/3 + Sine(5*freq)/5 + Sine(7*freq)/7 + Sine(9*freq)/9 + Sine(11*freq)/11
    else:
        # Simple Sine wave
        return Sine(freq=freq, mul=0.2)

# Function to start playing the note
def start_note(key, mode, octave):
    freq = key_to_freq.get(key)
    if freq and key not in active_notes:
        oct_mult = 2 ** octave 
        # Create the sine wave and store it in active_notes
        active_notes[key] = sound(oct_mult * freq, mode).out()

# Function to stop playing the note
def stop_note(key):
    if key in active_notes:
        active_notes[key].stop()  # Stop the sound
        del active_notes[key]  # Remove from active notes

# Main loop to check for key presses
mode = 1
octave = 0
o_up_pressed = False
o_down_pressed = False
m_was_pressed = False
try:

    print("######## PySynth ########")
    print("Controls:")
    print(" - Press 'm' to change mode: 1 -> Sine | 2 -> Saw | 3 -> Square")
    print(" - Press '1' for Octave Down")
    print(" - Press '2' for Octave Up")
    print("#########################")
    while True:
        # Handle mode switching on key release
        if keyboard.is_pressed('m'):
            if not m_was_pressed:
                m_was_pressed = True
        else:
            if m_was_pressed:
                m_was_pressed = False
                mode = (mode % 3) + 1
                print(f"Mode: {mode}")

        # Handle octave up
        if keyboard.is_pressed('2'):
            if not o_up_pressed:
                o_up_pressed = True
        else:
            if o_up_pressed:
                o_up_pressed = False
                octave += 1
                print(f"Octave Up: {octave}")

        # Handle octave down
        if keyboard.is_pressed('1'):
            if not o_down_pressed:
                o_down_pressed = True
        else:
            if o_down_pressed:
                o_down_pressed = False
                octave -= 1
                print(f"Octave Down: {octave}")

        for key in key_to_freq:
            # If the key is pressed
            if keyboard.is_pressed(key):
                # Start the corresponding note
                start_note(key, mode, octave)
            else:
                # Stop the note if key is released
                stop_note(key)
        # Sleep for a short time to prevent overloading CPU
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Exiting...")
    s.stop()