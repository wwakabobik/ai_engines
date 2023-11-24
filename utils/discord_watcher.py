# -*- coding: utf-8 -*-
"""
Filename: discord_watcher.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 20.11.2023
Last Modified: 20.11.2023

Description:
This file contains discord interactions to python API.
"""
from abc import ABC

from discord import Intents
from discord.ext import commands

from utils.logger_config import setup_logger


class DiscordWatcher(commands.Bot, ABC):  # pylint: disable=too-many-ancestors
    """Discord bot watcher for getting messages (images, urls, embeds) from a specific user."""

    def __init__(self, watch_user_id=None, **options):
        """
        Initialize DiscordWatcher class.

        :param command_prefix: The prefix for the bot.
        :param watch_user_id: The user ID to watch.
        :param options: The options for the bot.
        """
        super().__init__(command_prefix="/", intents=Intents.all(), **options)
        self.target_user_id = watch_user_id
        self.___logger = setup_logger("discord_watcher", "discord_watcher.log")
        self.___logger.info("DiscordWatcher initialized")

    async def on_ready(self):
        """This function is called when the bot is ready."""
        self.___logger.debug("We have logged in as %s", self.user)

    async def on_message(self, message):
        """
        This function is called when a message is created and sent.

        :param message: The message that was sent.
        :type message: discord.Message
        :return: The message content.
        :rtype: str
        """
        self.___logger.debug("Got a message from %s : %s : %s", message.author, message.author.id, message.content)
        if message.author.id == self.target_user_id:
            if "Waiting to start" not in message.content:
                self.___logger.debug("Found a message from the target user: %s", message.content)
                if message.attachments:
                    for attachment in message.attachments:
                        self.___logger.debug("Found an attachment: %s", attachment.url)
                        return attachment.url
                if message.embeds:
                    for embed in message.embeds:
                        self.___logger.debug("Found an embed: %s", embed.to_dict())
                        return embed.to_dict()
            else:
                self.___logger.debug("Found a message from the target user, but content is not ready yet...")
                return None
