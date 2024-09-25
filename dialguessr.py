import pyaudio
import numpy as np
from time import sleep
import argparse


def generate_samples(frequency: float, duration: float, sampling_rate: int = 44100):
    return (np.sin(2 * np.pi * np.arange(sampling_rate * duration) * frequency / sampling_rate)).astype(np.float32)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a random sequence of DTMF tones and ask the user to guess them.')
    parser.add_argument('-n', '--number_of_digits', type=int, default=1, help='Number of digits to generate.')
    args = parser.parse_args()

    sound_duration_s = .7
    pause_duration_s = 1
    volume = .5
    # we leave out the 1633 Hz frequency
    columns = np.array([1209, 1336, 1477])
    rows = np.array([697, 770, 852, 941])
    dial_pad = np.array(["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"])
    dp_frequencies = {str(p): (columns[i % 3], rows[i // 3]) for i, p in enumerate(dial_pad)}
    finished = False
    streak = 0
    tries = 0
    wins = 0
    while not finished:

        random_four_digits = np.random.randint(0, 10, args.number_of_digits)
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
            streak += 1
            tries += 1
            wins += 1
            status_string = f"{streak=} {wins}/{tries} {wins/tries:.2%}"
            win_message = f"You got it!"
            print(f"{win_message:<20} {status_string}")
        else:
            streak = 0
            tries += 1
            status_string = f"{streak=} {wins}/{tries} {wins / tries:.2%}"
            fail_message = f"Nope, it was {"".join(random_four_digits.astype(str))}"
            print(f"{fail_message:<20} {status_string}")
