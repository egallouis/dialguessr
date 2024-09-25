import pyaudio
import numpy as np
from time import sleep


def generate_samples(frequency: float, duration: float, sampling_rate: int = 44100):
    return (np.sin(2 * np.pi * np.arange(sampling_rate * duration) * frequency / sampling_rate)).astype(np.float32)


if __name__ == '__main__':
    sound_duration_s = .7
    pause_duration_s = 1
    volume = .5
    # we leave out the 1633 Hz frequency
    columns = np.array([1209, 1336, 1477])
    rows = np.array([697, 770, 852, 941])
    dial_pad = np.array(["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"])
    dp_frequencies = {str(p): (columns[i % 3], rows[i // 3]) for i, p in enumerate(dial_pad)}
    finished = False
    while not finished:
        random_four_digits = np.random.randint(0, 10, 4)
        frequencies = (dp_frequencies[str(digit)] for digit in random_four_digits)
        sampled_sounds = [generate_samples(frequency[0], sound_duration_s) +
                          generate_samples(frequency[1], sound_duration_s) for frequency in frequencies]

        p = pyaudio.PyAudio()
        fs = 44100  # sampling rate, Hz, must be integer
        # open stream using callback
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)
        # play. May repeat with different volume values (if done interactively)
        for sound in sampled_sounds:
            stream.write(volume * sound)
            sleep(pause_duration_s)

        dial_guess = input("write your guess: ")
        if dial_guess == "exit":
            finished = True
        elif dial_guess == "".join(random_four_digits.astype(str)):
            print("You got it!")
        else:
            print("Nope", "".join(random_four_digits.astype(str)))
