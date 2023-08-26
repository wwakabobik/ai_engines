# -*- coding: utf-8 -*-
"""
Filename: audio_recorder.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 25.08.2023
Last Modified: 26.08.2023

Description:
This file contains implementation for Audio Recorder
"""

import math
import os
import struct
import tempfile
import time
import uuid
import wave

import pyaudio
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment


def record_and_convert_audio(duration: int = 5, frequency_sample: int = 16000):
    """
    Records audio for a specified duration and converts it to MP3 format.

    This function records audio for a given duration (in seconds) with a specified frequency sample.
    The audio is then saved as a temporary .wav file, converted to .mp3 format, and the .wav file is deleted.
    The function returns the path to the .mp3 file.

    :param duration: The duration of the audio recording in seconds. Default is 5 seconds.
    :param frequency_sample: The frequency sample rate of the audio recording. Default is 16000 Hz.

    :return: The path to the saved .mp3 file.
    """
    print(f"Listening beginning for {duration}s...")
    recording = sd.rec(int(duration * frequency_sample), samplerate=frequency_sample, channels=1)
    sd.wait()  # Wait until recording is finished
    print("Recording complete!")
    temp_dir = tempfile.gettempdir()
    wave_file = f"{temp_dir}/{str(uuid.uuid4())}.wav"
    sf.write(wave_file, recording, frequency_sample)
    print(f"Temp audiofile saved: {wave_file}")
    audio = AudioSegment.from_wav(wave_file)
    os.remove(wave_file)
    mp3_file = f"{temp_dir}/{str(uuid.uuid4())}.mp3"
    audio.export(mp3_file, format="mp3")
    print(f"Audio converted to MP3 and stored into {mp3_file}")
    return mp3_file


# pylint: disable=too-many-instance-attributes
class AudioRecorder:
    """
    The AudioRecorder class is for managing an instance of the audio recording and conversion process.

    Parameters:
    pyaudio_obj (PyAudio): Instance of PyAudio. Default is pyaudio.PyAudio().
    threshold (int): The RMS threshold for starting the recording. Default is 15.
    channels (int): The number of channels in the audio stream. Default is 1.
    chunk (int): The number of frames per buffer. Default is 1024.
    f_format (int): The format of the audio stream. Default is pyaudio.paInt16.
    rate (int): The sample rate of the audio stream. Default is 16000 Hz.
    sample_width (int): The sample width (in bytes) of the audio stream. Default is 2.
    timeout_length (int): The length of the timeout for the recording (in seconds). Default is 2 seconds.
    temp_dir (str): The directory for storing the temporary .wav and .mp3 files. Default is the system's temporary dir.
    normalize (float): The normalization factor for the audio samples. Default is 1.0 / 32768.0.
    pa_input (bool): Specifies whether the stream is an input stream. Default is True.
    pa_output (bool): Specifies whether the stream is an output stream. Default is True.
    """

    def __init__(
        self,
        pyaudio_obj=pyaudio.PyAudio(),
        threshold=15,
        channels=1,
        chunk=1024,
        f_format=pyaudio.paInt16,
        rate=16000,
        sample_width=2,
        timeout_length=2,
        temp_dir=tempfile.gettempdir(),
        normalize=(1.0 / 32768.0),
        pa_input=True,
        pa_output=True,
    ):
        """
        General init.

        This method initializes an instance of the AudioRecorder class with the specified parameters.
        The default values are used for any parameters that are not provided.

        :param pyaudio_obj: Instance of PyAudio. Default is pyaudio.PyAudio().
        :param threshold: The RMS threshold for starting the recording. Default is 15.
        :param channels: The number of channels in the audio stream. Default is 1.
        :param chunk: The number of frames per buffer. Default is 1024.
        :param f_format: The format of the audio stream. Default is pyaudio.paInt16.
        :param rate: The sample rate of the audio stream. Default is 16000 Hz.
        :param sample_width: The sample width (in bytes) of the audio stream. Default is 2.
        :param timeout_length: The length of the timeout for the recording (in seconds). Default is 2 seconds.
        :param temp_dir: The directory for storing the temporary .wav and .mp3 files. Default is temp dir.
        :param normalize: The normalization factor for the audio samples. Default is 1.0 / 32768.0.
        :param pa_input: Specifies whether the stream is an input stream. Default is True.
        :param pa_output: Specifies whether the stream is an output stream. Default is True.
        """
        self.___pyaudio = pyaudio_obj
        self.___threshold = threshold
        self.___channels = channels
        self.___chunk = chunk
        self.___format = f_format
        self.___rate = rate
        self.___sample_width = sample_width
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
        """
        Initializes an audio stream with the specified parameters.

        This function uses PyAudio to open an audio stream with the given format, channels, rate, input, output,
        and frames per buffer.

        :param f_format: The format of the audio stream.
        :param channels: The number of channels in the audio stream.
        :param rate: The sample rate of the audio stream.
        :param pa_input: Specifies whether the stream is an input stream. A true value indicates an input stream.
        :param pa_output: Specifies whether the stream is an output stream. A true value indicates an output stream.
        :param frames_per_buffer: The number of frames per buffer.
        :type frames_per_buffer: int

        :return: The initialized audio stream.
        """
        return self.___pyaudio.open(
            format=f_format,
            channels=channels,
            rate=rate,
            input=pa_input,
            output=pa_output,
            frames_per_buffer=frames_per_buffer,
        )

    def record(self):
        """
        Starts recording audio when noise is detected.

        This function starts recording audio when noise above a certain threshold is detected.
        The recording continues for a specified timeout length.
        The recorded audio is then saved as a .wav file, converted to .mp3 format, and the .wav file is deleted.
        The function returns the path to the .mp3 file.

        :return: The path to the saved .mp3 file.
        """
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
        """
        Saves the recorded audio to a .wav file.

        This function saves the recorded audio to a .wav file with a unique filename.
        The .wav file is saved in the specified temporary directory.

        :param recording: The recorded audio data.

        :return: The path to the saved .wav file.
        """
        filename = os.path.join(self.___temp_dir, f"{str(uuid.uuid4())}.wav")

        wave_form = wave.open(filename, "wb")
        wave_form.setnchannels(self.___channels)
        wave_form.setsampwidth(self.___pyaudio.get_sample_size(self.___format))
        wave_form.setframerate(self.___rate)
        wave_form.writeframes(recording)
        wave_form.close()
        return filename

    def convert_to_mp3(self, filename):
        """
        Converts a .wav file to .mp3 format.

        This function converts a .wav file to .mp3 format. The .wav file is deleted after the conversion.
        The .mp3 file is saved with a unique filename in the specified temporary directory.

        :param filename: The path to the .wav file to be converted.

        :return: The path to the saved .mp3 file.
        """
        audio = AudioSegment.from_wav(filename)
        mp3_file_path = os.path.join(self.___temp_dir, f"{str(uuid.uuid4())}.mp3")
        audio.export(mp3_file_path, format="mp3")
        os.remove(filename)
        return mp3_file_path

    def listen(self):
        """
        Starts listening for audio.

        This function continuously listens for audio and starts recording when the
        RMS value of the audio exceeds a certain threshold.

        :return: The path to the saved .mp3 file if recording was triggered.
        """
        print("Listening beginning...")
        while True:
            mic_input = self.stream.read(self.___chunk)
            rms_val = self.rms(mic_input)
            if rms_val > self.___threshold:
                return self.record()

    def rms(self, frame):
        """
        Calculates the Root Mean Square (RMS) value of the audio frame.

        This function calculates the RMS value of the audio frame, which is a measure of the power in the audio signal.

        :param frame: The audio frame for which to calculate the RMS value.

        :return: The RMS value of the audio frame.
        """
        count = len(frame) / self.___sample_width
        f_format = "%dh" % count
        shorts = struct.unpack(f_format, frame)

        sum_squares = 0.0
        for sample in shorts:
            normal_sample = sample * self.___normalize
            sum_squares += normal_sample * normal_sample
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000
