# -*- coding: utf-8 -*-
"""
Filename: __main__.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 25.08.2023
Last Modified: 26.08.2023

Description:
This file is entry point for project-wide structure.
"""

# Engines
from openai_engine.chatgpt import ChatGPT  # pylint: disable=unused-import
from openai_engine.dalle import DALLE  # pylint: disable=unused-import

# Utils
from utils.tts import CustomTTS  # pylint: disable=unused-import
from utils.transcriptors import CustomTranscriptor  # pylint: disable=unused-import
from utils.translators import CustomTranslator  # pylint: disable=unused-import
from utils.audio_recorder import AudioRecorder, record_and_convert_audio  # pylint: disable=unused-import
from utils.logger_config import setup_logger  # pylint: disable=unused-import
from utils.other import is_heroku_environment  # pylint: disable=unused-import
