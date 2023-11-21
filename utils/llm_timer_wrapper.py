# -*- coding: utf-8 -*-
"""
Filename: llm_timer_wrapper.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 21.11.2023
Last Modified: 21.11.2023

Description:
This file contains the decorator for measuring time metrics of function execution.
"""

import time


class TimeMetricsWrapperSync:
    """Decorator for measuring time metrics of function execution"""

    def __init__(self, function):
        """
        Initialize TimeMetricsWrapper class.

        :param function: The function to measure.
        :type function: function
        """
        self.function = function

    def __call__(self, prompt, model=None):
        """
        Call the function and measure the time it takes to execute.

        :param prompt: The prompt to use for the function.
        :type prompt: str
        :param model: The model to use for the function.
        :type model: str
        :return: The metrics of the function.
        :rtype: dict
        """
        start_time = time.time()
        if model:
            result = self.function(prompt, model)
        else:
            result = self.function(prompt)
        end_time = time.time()

        elapsed_time = end_time - start_time
        words = len(result.split())
        chars = len(result)
        tokens = len(result) // 3

        word_speed = elapsed_time / words if words else 0
        char_speed = elapsed_time / chars if chars else 0
        token_speed = elapsed_time / tokens if tokens else 0

        metrix = {
            "elapsed_time": elapsed_time,
            "words": words,
            "chars": chars,
            "tokens": tokens,
            "word_speed": word_speed,
            "char_speed": char_speed,
            "token_speed": token_speed,
            "results": result,
        }

        return metrix


class TimeMetricsWrapperAsync:
    """Decorator for measuring time metrics of function execution"""

    def __init__(self, function):
        """
        Initialize TimeMetricsWrapper class.

        :param function: The function to measure.
        :type function: function
        """
        self.function = function

    async def __call__(self, prompt):
        """
        Call the function and measure the time it takes to execute.

        :param prompt: The prompt to use for the function.
        :type prompt: str
        :return: The metrics of the function.
        :rtype: dict
        """
        start_time = time.time()
        result = await self.function(prompt)
        end_time = time.time()

        elapsed_time = end_time - start_time
        words = len(result.split())
        chars = len(result)
        tokens = len(result) // 3

        word_speed = elapsed_time / words if words else 0
        char_speed = elapsed_time / chars if chars else 0
        token_speed = elapsed_time / tokens if tokens else 0

        metrix = {
            "elapsed_time": elapsed_time,
            "words": words,
            "chars": chars,
            "tokens": tokens,
            "word_speed": word_speed,
            "char_speed": char_speed,
            "token_speed": token_speed,
            "results": result,
        }

        return metrix
