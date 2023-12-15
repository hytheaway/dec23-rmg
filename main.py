import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from pydub import AudioSegment
from pydub.utils import make_chunks
# import librosa.display
from IPython.display import Audio
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import os
import random
import glob



def select_audio_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title='Select an audio file', filetypes=(('Audio Files', '*.wav *.mp3 *.aac *.flac *.ogg'), ('All Files', '*.*'))
    )
    root.destroy()

    return file_path


def chop_up_audio():
    files = glob.glob('outputs/*.wav')
    for f in files:
        os.remove(f)

    selected_file = select_audio_file()
    myaudio = AudioSegment.from_file(selected_file, 'wav')
    user_ms = bpm_to_ms()
    split_length_ms = user_ms
    splices = make_chunks(myaudio, split_length_ms)

    for i, split in enumerate(splices):
        splice_name = '{0}splice.wav'.format(i)
        print('exporting', splice_name)
        split.export('outputs/' + splice_name, format='wav')


# ----this makes the whole program go craaaaazy and hang while trying to process
# def change_pitch(audio, sample_rate, pitch_factor):
#     return librosa.effects.pitch_shift(audio, sample_rate, pitch_factor)


def combine_audio_files():
    dir_path = 'outputs/'
    count = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    count -= 1
    print('File count:', count)

    audio1 = AudioSegment.from_file('assets/0splice.wav', format='wav')
    audio2 = AudioSegment.from_file('assets/0splice.wav', format='wav')
    combined = audio1 + audio2

    j = 0
    value_list = []
    while j <= count-1:
        value_list.append(j)
        j += 1

    i = 0
    while i <= count-1:
        random_index = random.randrange(count-1)
        random_value = value_list[random_index]
        # coin_flip = random.randrange(0, 1)
        # if coin_flip == 0:
        #     continue
        # elif coin_flip == 1:
        #     data, sample_rate = sf.read('outputs/'+str(random_value)+'splice.wav')
        #     change_pitch(data, sample_rate, random.randint(15))
        #     sf.write('outputs/'+str(random_value)+'splice.wav', data, sample_rate)
        audio1 = AudioSegment.from_file('outputs/'+str(random_value)+'splice.wav', format='wav')
        combined = combined + audio1
        combined.export('combined_output.wav', format='wav')
        print('combined' + str(i))
        i += 1


def bpm_to_ms():
    application_window = tk.Tk()
    application_window.withdraw()
    answer = simpledialog.askstring("BPM-ometer", "What is the BPM?", parent=application_window)
    answer = int(answer)
    quarter_note_value = 60000/answer

    return quarter_note_value


def run_da_thing():
    chop_up_audio()
    combine_audio_files()


if __name__ == '__main__':
    run_da_thing()