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

def square_like_wave(freq, env):
    return (
        Sine(freq, mul=env * (1/1)) +
        Sine(3*freq, mul=env * (1/3)) +
        Sine(5*freq, mul=env * (1/5)) +
        Sine(7*freq, mul=env * (1/7)) +
        Sine(9*freq, mul=env * (1/9)) +
        Sine(11*freq, mul=env * (1/11))
    )

def sound(freq, mode):
    env = Adsr(attack=0.01, decay=0.2, sustain=0.5, release=0.1, dur=2, mul=0.5)
    if mode == 1:
        return Sine(freq=freq, mul=env), env
    elif mode == 2:
        return SuperSaw(freq=freq, mul=env), env
    elif mode == 3:
        return square_like_wave(freq, env), env
    elif mode == 4:
        return FM(carrier=freq, ratio=2, index=5, mul=env), env
    return None, None

# Function to start playing the note
def start_note(key, mode, octave):
    freq = key_to_freq.get(key)
    if freq and key not in active_notes:
        oct_mult = 2 ** octave 
        final_freq = oct_mult * freq
        # Create the sine wave and store it in active_notes
        snd, env = sound(final_freq, mode)
        snd.out()
        env.play()
        active_notes[key] = (snd, env)

# Function to stop playing the note
def stop_note(key):
    if key in active_notes:
        snd, env = active_notes[key]
        # Release the envelope
        env.stop()
        # Stop the sound
        snd.stop()
        del active_notes[key]

# Main loop to check for key presses
mode = 1
octave = 0
o_up_pressed = False
o_down_pressed = False
m_was_pressed = False
try:

    print("######## PySynth ########")
    print("Controls:")
    print(" - Press 'm' to change mode: 1 -> Sine | 2 -> Saw | 3 -> Square | 4 -> FM Modulation")
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
                mode = (mode % 4) + 1
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