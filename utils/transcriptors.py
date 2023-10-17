# -*- coding: utf-8 -*-
"""
Filename: transcriptors.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 25.08.2023
Last Modified: 17.10.2023

Description:
This module contains implementation for Custom Transcriptor
"""

import speech_recognition as sr


class CustomTranscriptor:
    """This is wrapper class for Google Transcriptor which uses microphone to get audio sample."""

    def __init__(self, language="en-EN"):
        """
        General init.

        :param language: Language, what needs to be transcripted.
        """
        self.___recognizer = sr.Recognizer()
        self.___source = sr.Microphone()
        self.___language = language

    @property
    def language(self):
        """
        Getter for language.

        :return: The language.
        """
        return self.___language

    @language.setter
    def language(self, value):
        """
        Setter for language.

        :param value: The language.
        """
        self.___language = value

    def transcript(self):
        """
        This function transcripts audio (from microphone recording) to text using Google transcriptor.

        :return: transcripted text (string).
        """
        print("Listening beginning...")
        with self.___source as source:
            audio = self.___recognizer.listen(source, timeout=5)

        user_input = None
        try:
            user_input = self.___recognizer.recognize_google(audio, language=self.language)
        except sr.UnknownValueError:
            print("Google Speech Recognition can't transcript audio")
        except sr.RequestError as error:
            print(f"Unable to fetch from resource Google Speech Recognition: {error}")
        except sr.WaitTimeoutError as error:
            print(f"Input timeout, only silence is get: {error}")
        return user_input
