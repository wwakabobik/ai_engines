# -*- coding: utf-8 -*-
"""
Filename: discord_interaction.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 20.11.2023
Last Modified: 20.11.2023

Description:
This file contains discord interactions to python API.
"""

import aiohttp


class DiscordInteractions:
    """"""
    def __init__(self, token, **kwargs):
        """
        Initialize DiscordInteractions class.

        :param token: The token to use for authorization.
        :param kwargs: The default parameters for the interaction.
        """
        self.token = token
        self.headers = {"authorization": self.token}
        self.url = "https://discord.com/api/v9/interactions"
        self.default_params = kwargs

    async def post_interaction(self, my_text_prompt, **kwargs):
        """
        Post any discord interaction.

        :param my_text_prompt: The text prompt to post.
        :type my_text_prompt: str
        :param kwargs: The parameters for the interaction.
        :return: The response from the interaction.
        """
        params = {**self.default_params, **kwargs}

        payload_data = {
            "type": 2,
            "application_id": params.get('application_id'),
            "guild_id": params.get('guild_id'),
            "channel_id": params.get('channel_id'),
            "session_id": params.get('session_id'),
            "data": {
                "version": params.get('version'),
                "id": params.get('interaction_id'),
                "name": "imagine",
                "type": 1,
                "options": [
                    {
                        "type": 3,
                        "name": "prompt",
                        "value": my_text_prompt
                    }
                ]
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload_data, headers=self.headers) as resp:
                if resp.status != 200 and resp.status != 204:
                    raise ValueError(f"Request failed with status code {resp.status}")
