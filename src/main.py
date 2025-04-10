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
    'a': 440.00,    # A4
    'w': 466.16,    # A#4/Bb4
    's': 493.88,    # B4
    'd': 523.25,    # C5
    'r': 554.37,    # C#5/Db5
    'f': 587.33,    # D5
    't': 622.25,    # D#5/Eb5
    'g': 659.25,    # E5
    'y': 698.46,    # F5
    'h': 739.99,    # F#5/Gb5
    'u': 783.99,    # G5
    'j': 830.61,    # G#5/Ab5
    'k': 880.00,    # A5
}

# Function to start playing the note
def start_note(key):
    freq = key_to_freq.get(key)
    if freq and key not in active_notes:
        # Create the sine wave and store it in active_notes
        active_notes[key] = Sine(freq=freq, mul=0.2).out()

# Function to stop playing the note
def stop_note(key):
    if key in active_notes:
        active_notes[key].stop()  # Stop the sound
        del active_notes[key]  # Remove from active notes

# Main loop to check for key presses
try:
    while True:
        for key in key_to_freq:
            # If the key is pressed
            if keyboard.is_pressed(key):
                # Start the corresponding note
                start_note(key)
            else:
                # Stop the note if key is released
                stop_note(key)
        # Sleep for a short time to prevent overloading CPU
        time.sleep(0.01)  

except KeyboardInterrupt:
    print("Exiting...")
    s.stop()