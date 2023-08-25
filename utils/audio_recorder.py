""" This module contains implementation for Audio Recorder """
import os
import struct
import tempfile
import time
import wave

# -*- coding: utf-8 -*-
import math
import pyaudio
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment


def record_and_convert_audio(duration=10, fs=44100):
    print(f"Listening beginning for {duration}s...")
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    print("Recording complete!")
    temp_dir = tempfile.gettempdir()
    wav_file_path = os.path.join(temp_dir, "my_audio.wav")
    sf.write(wav_file_path, myrecording, fs)
    print(f"Temp audiofile saved: {wav_file_path}")
    audio = AudioSegment.from_wav(wav_file_path)
    os.remove(os.path.join(temp_dir, "my_audio.wav"))
    mp3_file_path = os.path.join(temp_dir, "my_audio.mp3")
    audio.export(mp3_file_path, format="mp3")
    print("Audio converted to MP3 and stored into {mp3_file_path}")
    return mp3_file_path


class Recorder:
    def __init__(
        self,
        pyaudio_obj=pyaudio.PyAudio(),
        threshold=15,
        channels=1,
        chunk=1024,
        f_format=pyaudio.paInt16,
        rate=16000,
        swidth=2,
        timeout_length=2,
        temp_dir=tempfile.gettempdir(),
        normalize=(1.0 / 32768.0),
        pa_input=True,
        pa_output=True,
    ):
        self.___pyaudio = pyaudio_obj
        self.___threshold = threshold
        self.___channels = channels
        self.___chunk = chunk
        self.___format = f_format
        self.___rate = rate
        self.___swidth = swidth
        self.___timeout_length = timeout_length
        self.___temp_dir = temp_dir
        self.___normalize = normalize
        self.___input = pa_input
        self.___output = pa_output
        self.stream = self.init_stream(
            f_format=self.___format,
            channels=self.___channels,
            rate=self.___rate,
            pa_input=self.___input,
            pa_output=self.___output,
            frames_per_buffer=self.___chunk,
        )

    def init_stream(self, f_format, channels, rate, pa_input, pa_output, frames_per_buffer):
        return self.___pyaudio.open(
            format=f_format,
            channels=channels,
            rate=rate,
            input=pa_input,
            output=pa_output,
            frames_per_buffer=frames_per_buffer,
        )

    def record(self):
        print("Noise detected, recording beginning")
        rec = []
        current = time.time()
        end = time.time() + self.___timeout_length

        while current <= end:

            data = self.stream.read(self.___chunk)
            if self.rms(data) >= self.___threshold:
                end = time.time() + self.___timeout_length

            current = time.time()
            rec.append(data)
        filename = self.write(b"".join(rec))
        return self.convert_to_mp3(filename)

    def write(self, recording):
        n_files = len(os.listdir(self.___temp_dir))
        filename = os.path.join(self.___temp_dir, f"{n_files}.wav")

        wf = wave.open(filename, "wb")
        wf.setnchannels(self.___channels)
        wf.setsampwidth(self.p.get_sample_size(self.___format))
        wf.setframerate(self.___rate)
        wf.writeframes(recording)
        wf.close()
        return filename

    def convert_to_mp3(self, filename):
        audio = AudioSegment.from_wav(filename)
        mp3_file_path = os.path.join(self.___temp_dir, "my_audio.mp3")
        audio.export(mp3_file_path, format="mp3")
        os.remove(filename)
        return mp3_file_path

    def listen(self):
        print("Listening beginning...")
        while True:
            mic_input = self.stream.read(self.___chunk)
            rms_val = self.rms(mic_input)
            if rms_val > self.___threshold:
                return self.record()

    def rms(self, frame):
        count = len(frame) / self.___swidth
        f_format = "%dh" % count
        shorts = struct.unpack(f_format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * self.___normalize
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000
