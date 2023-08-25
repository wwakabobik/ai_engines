# -*- coding: utf-8 -*-
import os
import tempfile
from time import sleep

from gtts import gTTS
from mpyg321.mpyg321 import MPyg321Player
from mutagen.mp3 import MP3
from pydub import AudioSegment
from pyttsx4 import init as pyttsx_init


class CustomTTS:
    def __init__(
        self, method="google", lang="en", speedup=1.3, frame=0.1, voice="com.apple.voice.enhanced.ru-RU.Katya"
    ):
        self.___method = method
        self.___player = MPyg321Player()
        self.___pytts = pyttsx_init()
        self.___lang = lang
        self.___voice = voice
        self.___speedup = speedup
        self.___frame = frame

    def __process_via_gtts(self, answer):
        temp_dir = tempfile.gettempdir()
        # gtts
        tts = gTTS(answer, lang=self.___lang)
        tts.save(f"{temp_dir}/raw.mp3")
        audio = AudioSegment.from_file(f"{temp_dir}/raw.mp3", format="mp3")
        new = audio.speedup(1.3)  # speed up by 2x
        os.remove(f"{temp_dir}/raw.mp3")
        new.export(f"{temp_dir}/response.mp3", format="mp3")
        # player
        self.___player.play_song(f"{temp_dir}/response.mp3")
        audio = MP3(f"{temp_dir}/response.mp3")
        sleep(audio.info.length)
        self.___player.stop()
        os.remove(f"{temp_dir}/response.mp3")

    def __process_via_pytts(self, answer):
        engine = self.___pytts
        engine.setProperty("voice", self.___voice)
        engine.say(answer)
        engine.startLoop(False)

        while engine.isBusy():
            engine.iterate()
            sleep(0.1)

        engine.endLoop()

    async def process(self, answer):
        if "google" in self.___method:
            self.__process_via_gtts(answer)
        else:
            self.__process_via_pytts(answer)

    def get_pytts_voices_list(self):
        return self.___pytts.getProperty("voices")
