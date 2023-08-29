# -*- coding: utf-8 -*-
"""
Filename: chatgpt.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 25.08.2023
Last Modified: 26.08.2023

Description:
This file contains implementation for ChatGPT
"""

import json
import logging

import openai

from openai_engine.models import COMPLETIONS, TRANSCRIPTIONS, TRANSLATIONS


class GPTStatistics:
    """
    The GPTStatistics class is for managing an instance of the GPTStatistics model.

    Parameters:
    prompt_tokens (int): The number of tokens in the prompt. Default is 0.
    completion_tokens (int): The number of tokens in the completion. Default is 0.
    total_tokens (int): The total number of tokens. Default is 0.
    """

    def __init__(
        self,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        total_tokens: int = 0,
    ):
        """
        Constructs all the necessary attributes for the GPTStatistics object.

        :param prompt_tokens: The number of tokens in the prompt. Default is 0.
        :param completion_tokens: The number of tokens in the completion. Default is 0.
        :param total_tokens: The total number of tokens. Default is 0.
        """
        self.___prompt_tokens = prompt_tokens
        self.___completion_tokens = completion_tokens
        self.___total_tokens = total_tokens

    @property
    def prompt_tokens(self):
        """
        Getter for prompt_tokens.

        :return: The prompt tokens.
        """
        return self.___prompt_tokens

    @prompt_tokens.setter
    def prompt_tokens(self, value):
        """
        Setter for prompt_tokens.

        :param value: The prompt tokens.
        """
        self.___prompt_tokens = value

    @property
    def completion_tokens(self):
        """
        Getter for completion_tokens.

        :return: The completion tokens.
        """
        return self.___completion_tokens

    @completion_tokens.setter
    def completion_tokens(self, value):
        """
        Setter for completion_tokens.

        :param value: The completion tokens.
        """
        self.___completion_tokens = value

    @property
    def total_tokens(self):
        """
        Getter for completion_tokens.

        :return: The completion tokens.
        """
        return self.___total_tokens

    @total_tokens.setter
    def total_tokens(self, value):
        """
        Setter for total_tokens.

        :param value: The total tokens.
        """
        self.___total_tokens = value

    def add_prompt_tokens(self, value):
        """
        Adder for prompt_tokens.

        :param value: The prompt tokens.
        """
        self.prompt_tokens += value

    def add_completion_tokens(self, value):
        """
        Adder for completion_tokens.

        :param value: The completion tokens.
        """
        self.completion_tokens += value

    def add_total_tokens(self, value):
        """
        Adder for total_tokens.

        :param value: The total tokens.
        """
        self.total_tokens += value

    def set_tokens(self, prompt_tokens, completion_tokens, total_tokens):
        """
        Sets all tokens statistics in bulk

        :param prompt_tokens: The prompt tokens.
        :param completion_tokens: The prompt tokens.
        :param total_tokens: The prompt tokens.
        """
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens

    def add_tokens(self, prompt_tokens, completion_tokens, total_tokens):
        """
        Adds all tokens statistics in bulk

        :param prompt_tokens: The prompt tokens.
        :param completion_tokens: The prompt tokens.
        :param total_tokens: The prompt tokens.
        """
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.total_tokens += total_tokens

    def get_tokens(self):
        """
        Returns a dictionary of the class attributes and their values.

        :return: dict with tokens statistics
        """
        return {
            "prompt_tokens": self.___prompt_tokens,
            "completion_tokens": self.___completion_tokens,
            "total_tokens": self.___total_tokens,
        }


# pylint: disable=too-many-instance-attributes,too-many-public-methods
class ChatGPT:
    """
    The ChatGPT class is for managing an instance of the ChatGPT model.

    Parameters:
    auth_token (str): Authentication bearer token. Required.
    organization (str): Organization uses auth toke. Required.
    model (str): The name of the model, Default is 'gpt-4'.
    choices (int, optional): The number of response options. Default is 1.
    temperature (float, optional): The temperature of the model's output. Default is 1.
    top_p (float, optional): The top-p value for nucleus sampling. Default is 1.
    stream (bool, optional): If True, the model will return intermediate results. Default is False.
    stop (str, optional): The stop sequence at which the model should stop generating further tokens. Default is None.
    max_tokens (int, optional): The maximum number of tokens in the output. Default is 1024.
    presence_penalty (float, optional): The penalty for new token presence. Default is 0.
    frequency_penalty (float, optional): The penalty for token frequency. Default is 0.
    logit_bias (map, optional): The bias for the logits before sampling. Default is None.
    user (str, optional): The user ID. Default is ''.
    functions (list, optional): The list of functions. Default is None.
    function_call (str, optional): The function call. Default is None.
    function_dict (dict, optional): Dict of functions. Default is None.
    history_length (int, optional): Length of history. Default is 5.
    chats (dict, optional): Chats dictionary, contains all chat. Default is None.
    current_chat (str, optional): Default chat will be used. Default is None.
    prompt_method (bool, optional): prompt method. Use messages if False, otherwise - prompt. Default if False.
    logger (logging.Logger, optional): default logger. Default is None.
    statistic (GPTStatistics, optional): statistics logger. If none, will be initialized with zeros.
    system_settings (str, optional): general instructions for chat. Default is None.
    echo    # TODO
    best_of # TODO
    suffix  # TODO
    """

    def __init__(
        # pylint: disable=too-many-locals
        self,
        auth_token: str,
        organization: str,
        model: str = COMPLETIONS[0],
        choices: int = 1,
        temperature: float = 1,
        top_p: float = 1,
        stream: bool = False,
        stop: str = None,
        max_tokens: int = 1024,
        presence_penalty: float = 0,
        frequency_penalty: float = 0,
        logit_bias: map = None,
        user: str = "",
        functions: list = None,
        function_call: str = None,
        history_length: int = 5,
        chats: dict = None,
        current_chat: str = None,
        prompt_method: bool = False,
        logger: logging.Logger = None,
        statistics: GPTStatistics = GPTStatistics(),
        system_settings: str = None,
        function_dict: dict = None,
    ):
        """
        General init

        :param auth_token (str): Authentication bearer token. Required.
        :param organization (str): Organization uses auth toke. Required.
        :param model: The name of the model.
        :param choices: The number of response options. Default is 1.
        :param temperature: The temperature of the model's output. Default is 1.
        :param top_p: The top-p value for nucleus sampling. Default is 1.
        :param stream: If True, the model will return intermediate results. Default is False.
        :param stop: The stop sequence at which the model should stop generating further tokens. Default is None.
        :param max_tokens: The maximum number of tokens in the output. Default is 1024.
        :param presence_penalty: The penalty for new token presence. Default is 0.
        :param frequency_penalty: The penalty for token frequency. Default is 0.
        :param logit_bias: The bias for the logits before sampling. Default is None.
        :param user: The user ID. Default is ''.
        :param functions: The list of functions. Default is None.
        :param function_call: The function call. Default is None.
        :param function_dict: Dict of functions. Default is None.
        :param history_length: Length of history. Default is 5.
        :param chats: Chats dictionary, contains all chat. Default is None.
        :param current_chat: Default chat will be used. Default is None.
        :param prompt_method: prompt method. Use messages if False, otherwise - prompt. Default if False.
        :param logger: default logger. Default is None.
        :param statistics: statistics logger. If none, will be initialized with zeros.
        :param system_settings: general system instructions for bot. Default is ''.
        """
        self.___model = model
        self.___choices = choices
        self.___temperature = temperature
        self.___top_p = top_p
        self.___stream = stream
        self.___stop = stop
        self.___max_tokens = max_tokens
        self.___presence_penalty = presence_penalty
        self.___frequency_penalty = frequency_penalty
        self.___logit_bias = logit_bias
        self.___user = user
        self.___functions = functions
        self.___function_call = function_call
        self.___function_dict = function_dict
        self.___history_length = history_length
        self.___chats = chats if chats else {}
        self.___current_chat = current_chat
        self.___prompt_method = prompt_method
        self.___set_auth(auth_token, organization)
        self.___logger = logger
        self.___statistics = statistics
        self.___system_settings = system_settings if system_settings else ""

    @staticmethod
    def ___set_auth(token, organization):
        """
        Method to set auth bearer.

        :param token: authentication bearer token.
        :param organization: organization, which drives the chat.
        """
        openai.api_key = token
        openai.organization = organization

    @property
    def model(self):
        """
        Getter for model.

        :return: The name of the model.
        """
        return self.___model

    @model.setter
    def model(self, value):
        """
        Setter for model.

        :param value: The new name of the model.
        """
        self.___model = value

    @property
    def choices(self):
        """
        Getter for choices.

        :return: The number of response options.
        """
        return self.___choices

    @choices.setter
    def choices(self, value):
        """
        Setter for choices.

        :param value: The new number of response options.
        """
        self.___choices = value

    @property
    def temperature(self):
        """
        Getter for temperature.

        :return: The temperature of the model's output.
        """
        return self.___temperature

    @temperature.setter
    def temperature(self, value):
        """
        Setter for temperature.

        :param value: The new temperature of the model's output.
        """
        self.___temperature = value

    @property
    def top_p(self):
        """
        Getter for top_p.

        :return: The top-p value for nucleus sampling.
        """
        return self.___top_p

    @top_p.setter
    def top_p(self, value):
        """
        Setter for top_p.

        :param value: The new top-p value for nucleus sampling.
        """
        self.___top_p = value

    @property
    def stream(self):
        """
        Getter for stream.

        :return: If True, the model will return intermediate results.
        """
        return self.___stream

    @stream.setter
    def stream(self, value):
        """
        Setter for stream.

        :param value: The new value for stream.
        """
        self.___stream = value

    @property
    def stop(self):
        """
        Getter for stop.

        :return: The stop sequence at which the model should stop generating further tokens.
        """
        return self.___stop

    @stop.setter
    def stop(self, value):
        """
        Setter for stop.

        :param value: The new stop sequence.
        """
        self.___stop = value

    @property
    def max_tokens(self):
        """
        Getter for max_tokens.

        :return: The maximum number of tokens in the output.
        """
        return self.___max_tokens

    @max_tokens.setter
    def max_tokens(self, value):
        """
        Setter for max_tokens.

        :param value: The new maximum number of tokens in the output.
        """
        self.___max_tokens = value

    @property
    def presence_penalty(self):
        """
        Getter for presence_penalty.

        :return: The penalty for new token presence.
        """
        return self.___presence_penalty

    @presence_penalty.setter
    def presence_penalty(self, value):
        """
        Setter for presence_penalty.

        :param value: The new penalty for new token presence.
        """
        self.___presence_penalty = value

    @property
    def frequency_penalty(self):
        """
        Getter for frequency_penalty.

        :return: The penalty for token frequency.
        """
        return self.___frequency_penalty

    @frequency_penalty.setter
    def frequency_penalty(self, value):
        """
        Setter for frequency_penalty.

        :param value: The new penalty for token frequency.
        """
        self.___frequency_penalty = value

    @property
    def logit_bias(self):
        """
        Getter for logit_bias.

        :return: The bias for the logits before sampling.
        """
        return self.___logit_bias

    @logit_bias.setter
    def logit_bias(self, value):
        """
        Setter for logit_bias.

        :param value: The new bias for the logits before sampling.
        """
        self.___logit_bias = value

    @property
    def user(self):
        """
        Getter for user.

        :return: The user ID.
        """
        return self.___user

    @user.setter
    def user(self, value):
        """
        Setter for user.

        :param value: The new user ID.
        """
        self.___user = value

    @property
    def functions(self):
        """
        Getter for functions.

        :return: The list of functions.
        """
        return self.___functions

    @functions.setter
    def functions(self, value):
        """
        Setter for functions.

        :param value: The new list of functions.
        """
        self.___functions = value

    @property
    def function_call(self):
        """
        Getter for function_call.

        :return: The function call.
        """
        return self.___function_call

    @function_call.setter
    def function_call(self, value):
        """
        Setter for function_call.

        :param value: The new function call.
        """
        self.___function_call = value

    @property
    def function_dict(self):
        """
        Getter for function_dict.

        :return: The function dict.
        """
        return self.___function_dict

    @function_dict.setter
    def function_dict(self, value):
        """
        Setter for function_dict.

        :param value: The new function dict.
        """
        self.___function_dict = value

    @property
    def history_length(self):
        """
        Getter for history_length.

        :return: The history length.
        """
        return self.___history_length

    @history_length.setter
    def history_length(self, value):
        """
        Setter for history_length.

        :param value: The new history length.
        """
        self.___history_length = value

    @property
    def chats(self):
        """
        Getter for chats.

        :return: The chats.
        """
        return self.___chats

    @chats.setter
    def chats(self, value):
        """
        Setter for chats.

        :param value: The new chats.
        """
        self.___chats = value

    @property
    def current_chat(self):
        """
        Getter for current_chat.

        :return: The current chat.
        """
        return self.___current_chat

    @current_chat.setter
    def current_chat(self, value):
        """
        Setter for current_chat.

        :param value: The current chat.
        """
        self.___current_chat = value

    @property
    def prompt_method(self):
        """
        Getter for prompt_method.

        :return: The prompt method.
        """
        return self.___prompt_method

    @prompt_method.setter
    def prompt_method(self, value):
        """
        Setter for prompt_method.

        :param value: The prompt method.
        """
        self.___prompt_method = value

    @property
    def system_settings(self):
        """
        Getter for system_settings.

        :return: The system settings method.
        """
        return self.___system_settings

    @system_settings.setter
    def system_settings(self, value):
        """
        Setter for system_settings.

        :param value: The system settings.
        """
        self.___system_settings = value

    @property
    def logger(self):
        """
        Getter for logger.

        :return: The logger object.
        """
        return self.___logger

    @logger.setter
    def logger(self, value):
        """
        Setter for logger.

        :param value: The new logger object.
        """
        self.___logger = value

    async def process_chat(self, prompt, default_choice=0, chat_name=None):
        """
        Creates a new chat completion for the provided messages and parameters.

        :param prompt: The prompt to pass to the model.
        :param default_choice: Default number of choice to monitor for stream end. By default, is None.
        :param chat_name: Chat name for function tracking. Should be handled by caller. By default, is None.

        :return: Returns answers by chunk if 'stream' is false True, otherwise return complete answer.
        """
        # pylint: disable=too-many-branches
        # Prepare parameters
        params = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "n": self.choices,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "user": self.user,
            "functions": self.functions,
            "function_call": self.function_call,
            "stream": self.stream,
        }

        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}

        # Add 'prompt' or 'messages' parameter
        if self.prompt_method:
            params["prompt"] = prompt
        else:
            params["messages"] = prompt

        # Get response
        func_response = None
        func_call = dict()
        if self.stream:
            try:
                async for chunk in await openai.ChatCompletion.acreate(**params):
                    if "function_call" in chunk["choices"][default_choice]["delta"]:
                        raw_call = chunk["choices"][default_choice]["delta"]["function_call"]
                        for key, value in raw_call.items():
                            if key in func_call and isinstance(value, str):
                                func_call[key] += value
                            elif key in func_call and isinstance(func_call[key], dict) and isinstance(value, dict):
                                func_call[key].update(value)
                            else:
                                func_call[key] = value
                    if chunk["choices"][default_choice]["finish_reason"] is not None:
                        if chunk["choices"][default_choice]["finish_reason"] == 'function_call':
                            func_response = await self.process_function(function_call=func_call)
                        break
                    if "content" in chunk["choices"][default_choice]["delta"]:
                        if chunk["choices"][default_choice]["delta"]["content"]:
                            yield chunk
                        else:
                            continue
                    else:
                        continue
            except GeneratorExit:
                pass
            try:
                if func_response:
                    # Save to history
                    if chat_name:
                        self.chats[chat_name].append(func_response)
                    # Add new prompt
                    if self.prompt_method:
                        params.pop("prompt", None)
                        params["messages"] = list()
                        params["messages"].append(func_response)
                    else:
                        params["messages"].append(func_response)
                    async for chunk in await openai.ChatCompletion.acreate(**params):
                        yield chunk
                        if chunk["choices"][default_choice]["finish_reason"] is not None:
                            break
            except GeneratorExit:
                pass
        else:
            response = await openai.ChatCompletion.acreate(**params)
            if response["choices"][default_choice]["finish_reason"] == 'function_call':
                func_response = await self.process_function(
                    function_call=response["choices"][default_choice]["message"]["function_call"]
                )
            try:
                if func_response:
                    # Save to history
                    if chat_name:
                        self.chats[chat_name].append(func_response)
                    # Add new prompt
                    if self.prompt_method:
                        params.pop("prompt", None)
                        params["messages"] = list()
                        params["messages"].append(func_response)
                    else:
                        params["messages"].append(func_response)
                    response = await openai.ChatCompletion.acreate(**params)
                    yield response
                else:
                    yield response
            except GeneratorExit:
                pass

    async def __handle_chat_name(self, chat_name, prompt):
        """
        Handles the chat name. If chat_name is None, sets it to the first 40 characters of the prompt.
        If chat_name is not present in self.chats, adds it.

        :param chat_name: Name of the chat.
        :param prompt: Message from the user.
        :return: Processed chat name.
        """
        if chat_name is None:
            chat_name = prompt[:40]
            self.current_chat = chat_name
        if chat_name not in self.chats:
            self.chats[chat_name] = []
        return chat_name

    async def chat(self, prompt, chat_name=None, default_choice=0):
        """
        Wrapper for the process_chat function. Adds new messages to the chat and calls process_chat.

        :param prompt: Message from the user.
        :param chat_name: Name of the chat. If None, uses self.current_chat.
        :param default_choice: Index of the model's response choice.
        """
        # pylint: disable=too-many-branches
        # Call process_chat
        full_prompt = ""
        if self.prompt_method:
            try:
                async for response in self.process_chat(prompt=prompt, default_choice=default_choice):
                    if isinstance(response, dict):
                        finish_reason = response["choices"][default_choice].get("finish_reason", "")
                        yield response
                        if self.stream:
                            if "content" in response["choices"][default_choice]["delta"].keys():
                                full_prompt += response["choices"][default_choice]["delta"]["content"]
                        else:
                            full_prompt += response["choices"][default_choice]["message"]["content"]
                        if finish_reason is not None:
                            yield ""
                    else:
                        break
            except GeneratorExit:
                pass
        else:
            # Set chat_name
            chat_name = chat_name if chat_name is not None else self.current_chat
            chat_name = await self.__handle_chat_name(chat_name, prompt)
            # Add new message to chat
            self.chats[chat_name].append({"role": "user", "content": prompt})
            # Get last 'history_length' messages
            messages = self.chats[chat_name][-self.history_length:]
            messages.insert(0, {"role": "system", "content": self.system_settings})

            try:
                async for response in self.process_chat(
                    prompt=messages, default_choice=default_choice, chat_name=chat_name
                ):
                    if isinstance(response, dict):
                        finish_reason = response["choices"][default_choice].get("finish_reason", "")
                        yield response
                        if self.stream:
                            if "content" in response["choices"][default_choice]["delta"].keys():
                                full_prompt += response["choices"][default_choice]["delta"]["content"]
                        else:
                            full_prompt += response["choices"][default_choice]["message"]["content"]
                        if finish_reason is not None:
                            yield ""
                    else:
                        break
            except GeneratorExit:
                pass

        # Add last response to chat
        self.chats[chat_name].append({"role": "assistant", "content": full_prompt})

    async def str_chat(self, prompt, chat_name=None, default_choice=0):
        """
        Wrapper for the chat function. Returns only the content of the message.

        :param prompt: Message from the user.
        :param chat_name: Name of the chat. If None, uses self.current_chat.
        :param default_choice: Index of the model's response choice.

        :return: Content of the message.
        """
        try:
            async for response in self.chat(prompt, chat_name, default_choice):
                if isinstance(response, dict):
                    if self.stream:
                        if "content" in response["choices"][default_choice]["delta"].keys():
                            yield response["choices"][default_choice]["delta"]["content"]
                        else:
                            yield ""
                    else:
                        yield response["choices"][default_choice]["message"]["content"]
                else:
                    break
        except GeneratorExit:
            pass

    async def transcript(self, file, prompt=None, language="en", response_format="text"):
        """
        Wrapper for the transcribe function. Returns only the content of the message.

        :param file: Path with filename to transcript.
        :param prompt: Previous prompt. Default is None.
        :param language: Language on which audio is. Default is 'en'.
        :param response_format: default response format, by default is 'text'.
                               Possible values are: json, text, srt, verbose_json, or vtt.


        :return: transcription (text, json, srt, verbose_json or vtt)
        """
        kwargs = {}
        if prompt is not None:
            kwargs["prompt"] = prompt
        return await openai.Audio.atranscribe(
            model=TRANSCRIPTIONS[0],
            file=file,
            language=language,
            response_format=response_format,
            temperature=self.temperature,
            **kwargs,
        )

    async def translate(self, file, prompt=None, response_format="text"):
        """
        Wrapper for the translate function. Returns only the content of the message.

        :param file: Path with filename to transcript.
        :param prompt: Previous prompt. Default is None.
        :param response_format: default response format, by default is 'text'.
                               Possible values are: json, text, srt, verbose_json, or vtt.


        :return: transcription (text, json, srt, verbose_json or vtt)
        """
        kwargs = {}
        if prompt is not None:
            kwargs["prompt"] = prompt
        return await openai.Audio.atranslate(
            model=TRANSLATIONS[0], file=file, response_format=response_format, temperature=self.temperature, **kwargs
        )

    async def process_function(self, function_call):
        """
        Process function requested by ChatGPT.

        :param function_call: Function name and arguments. In JSON format.

        :return: transcription (text, json, srt, verbose_json or vtt)
        """
        function_name = function_call["name"]
        function_to_call = self.function_dict[function_name]
        function_response = function_to_call(**json.loads(function_call["arguments"]))
        return {"role": "function", "name": function_name, "content": function_response}
