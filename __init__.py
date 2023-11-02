# -*- coding: utf-8 -*-
"""
Filename: __main__.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 25.08.2023
Last Modified: 17.10.2023

Description:
This file is init point for project-wide structure.
"""

from .utils.tts import CustomTTS  # pylint: disable=unused-import
from .utils.transcriptors import CustomTranscriptor  # pylint: disable=unused-import
from .utils.translators import CustomTranslator  # pylint: disable=unused-import
from .utils.audio_recorder import AudioRecorder, record_and_convert_audio  # pylint: disable=unused-import
from .utils.logger_config import setup_logger  # pylint: disable=unused-import
from .utils.other import is_heroku_environment  # pylint: disable=unused-import
