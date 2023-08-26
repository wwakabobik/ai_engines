# -*- coding: utf-8 -*-
"""
Filename: models.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 25.08.2023
Last Modified: 25.08.2023

Description:
This file contains OpenAI constants
"""

COMPLETIONS = (
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0613",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
)
TRANSCRIPTIONS = ("whisper-1",)
TRANSLATIONS = ("whisper-1",)
FINE_TUNES = ("davinci", "curie", "babbage", "ada")
EMBEDDINGS = (
    "text-embedding-ada-002",
    "text-similarity-*-001",
    "text-search-*-*-001",
    "code-search-*-*-001"
)
MODERATIONS = ("text-moderation-stable", "text-moderation-latest")
