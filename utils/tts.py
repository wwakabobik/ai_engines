# -*- coding: utf-8 -*-
"""
Filename: tts.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 25.08.2023
Last Modified: 25.08.2023

Description:
This module contains implementation for Text-to-Speach tools
"""

import os
import tempfile
from time import sleep
from uuid import uuid4

from gtts import gTTS
from mpyg321.mpyg321 import MPyg321Player
from mutagen.mp3 import MP3
from pydub import AudioSegment
from pyttsx4 import init as pyttsx_init


class CustomTTS:
    """
    The GPTStatistics class is for managing an instance of the Custom Text-to-Speach models.

    Parameters:
    method (str): Default method to use TTS. Default is 'google'.
    lang: language in ISO 639-1 format. Default is 'en'.
    speedup (float): Speedup ratio. Default is 1.3.
    frame (float): audio sample frame in seconds. Default is 0.1.
    voice (str): default TTS voice to use. Default is 'com.apple.voice.enhanced.ru-RU.Katya'
    """

    def __init__(
        self, method="google", lang="en", speedup=1.3, frame=0.1, voice="com.apple.voice.enhanced.ru-RU.Katya"
    ):
        """
        General init.

        :param method: Default method to use TTS. Default is 'google'.
        :param lang: language in ISO 639-1 format. Default is 'en'.
        :param speedup: Speedup ratio. Default is 1.3.
        :param frame: audio sample frame in seconds. Default is 0.1.
        :param voice: default TTS voice to use. Default is 'com.apple.voice.enhanced.ru-RU.Katya'
        """
        self.___method = method
        self.___player = MPyg321Player()
        self.___pytts = pyttsx_init()
        self.___lang = lang
        self.___voice = voice
        self.___speedup = speedup
        self.___frame = frame

    def __process_via_gtts(self, text):
        """
        Converts text to speach using Google text-to-speach method

        :param text: Text needs to be converted to speach.
        """
        temp_dir = tempfile.gettempdir()
        # gtts
        tts = gTTS(text, lang=self.___lang)
        raw_file = f"{temp_dir}/{str(uuid4())}.mp3"
        tts.save(raw_file)
        audio = AudioSegment.from_file(raw_file, format="mp3")
        new = audio.speedup(self.___speedup)
        os.remove(raw_file)
        response_file = f"{temp_dir}/{str(uuid4())}.mp3"
        new.export(response_file, format="mp3")
        # player
        self.___player.play_song(response_file)
        audio = MP3(response_file)
        sleep(audio.info.length)
        self.___player.stop()
        os.remove(response_file)

    def __process_via_pytts(self, text):
        """
        Converts text to speach using python-tts text-to-speach method

        :param text: Text needs to be converted to speach.
        """
        engine = self.___pytts
        engine.setProperty("voice", self.___voice)
        engine.say(text)
        engine.startLoop(False)

        while engine.isBusy():
            engine.iterate()
            sleep(self.___frame)

        engine.endLoop()

    def get_pytts_voices_list(self):
        """
        Returns list of possible voices

        :return: (list) of possible voices
        """
        return self.___pytts.getProperty("voices")

    async def process(self, text):
        """
        Converts text to speach using pre-defined model

        :param text: Text needs to be converted to speach.
        """
        if "google" in self.___method:
            self.__process_via_gtts(text)
        else:
            self.__process_via_pytts(text)