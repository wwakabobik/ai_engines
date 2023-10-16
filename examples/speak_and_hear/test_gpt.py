# -*- coding: utf-8 -*-
"""
Filename: chatgpt.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 25.08.2023
Last Modified: 25.08.2023

Description:
This file contains testing procedures for ChatGPt experiments
"""

import string
import sys

import asyncio

from utils.audio_recorder import AudioRecorder
from utils.transcriptors import CustomTranscriptor
from utils.tts import CustomTTS

from ..creds import oai_token, oai_organization
from ...openai_api import ChatGPT


gpt = ChatGPT(auth_token=oai_token, organization=oai_organization, model="gpt-3.5-turbo")
gpt.max_tokens = 200
gpt.stream = True


tts = CustomTTS(method="google", lang="en")

# queues
prompt_queue = asyncio.Queue()
tts_queue = asyncio.Queue()


async def ask_chat(user_input):
    full_response = ""
    word = ""
    async for response in gpt.str_chat(user_input):
        for char in response:
            word += char
            if char in string.whitespace or char in string.punctuation:
                if word:
                    await prompt_queue.put(word)
                    word = ""
            sys.stdout.write(char)
            sys.stdout.flush()
            full_response += char
    print("\n")
    return full_response


async def tts_task():
    limit = 5
    empty_counter = 0
    while True:
        if prompt_queue.empty():
            empty_counter += 1
        if empty_counter >= 3:
            limit = 5
            empty_counter = 0
        words = []
        # Get all available words
        limit_counter = 0
        while len(words) < limit:
            try:
                word = await asyncio.wait_for(prompt_queue.get(), timeout=0.5)
                words.extend(word.split())
                if len(words) >= limit:
                    break
            except asyncio.TimeoutError:
                limit_counter += 1
                if limit_counter >= 10:
                    limit = 1

        # If we have at least limit words or queue was empty 3 times, process them
        if len(words) >= limit:
            text = " ".join(words)
            await tts.process(text)
            limit = 1


async def tts_sentence_task():
    punctuation_marks = ".?!,;:"
    sentence = ""
    while True:
        try:
            word = await asyncio.wait_for(prompt_queue.get(), timeout=0.5)
            sentence += " " + word
            # If the last character is a punctuation mark, process the sentence
            if sentence[-1] in punctuation_marks:
                await tts_queue.put(sentence)
                sentence = ""
        except Exception as error:
            pass


async def tts_worker():
    while True:
        try:
            sentence = await tts_queue.get()
            if sentence:
                await tts.process(sentence)
                tts_queue.task_done()
        except Exception as error:
            pass


async def get_user_input():
    while True:
        try:
            user_input = input()
            if user_input.lower() == "[done]":
                break
            else:
                await ask_chat(user_input)
        except KeyboardInterrupt:
            break


async def main():
    asyncio.create_task(tts_sentence_task())
    asyncio.create_task(tts_worker())
    method = "google"

    while True:
        try:
            if "google" not in method:
                file_path = AudioRecorder().listen()
                with open(file_path, "rb") as f:
                    transcript = await gpt.transcript(file=f, language="en")
            else:
                transcript = CustomTranscriptor(language="en-US").transcript()
                pass
            if transcript:
                print(f"User: {transcript}")
                #translate = CustomTranslator(source='ru', target='en').translate(transcript)
                #print(translate)
                response = await ask_chat(transcript)
        except KeyboardInterrupt:
            break


asyncio.run(main())

