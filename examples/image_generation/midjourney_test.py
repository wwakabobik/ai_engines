# -*- coding: utf-8 -*-
"""
Filename: leonardo_test.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 15.10.2023
Last Modified: 20.11.2023

Description:
This file contains testing procedures for Midjourney experiments
"""

import asyncio

# pylint: disable=import-error
from examples.creds import discord_watcher_token, discord_midjourney_payload  # type: ignore
from utils.discord_interactions import DiscordInteractions
from utils.discord_watcher import DiscordWatcher


# Usage
async def main():
    """Main function"""
    prompt = "a beautiful necromancer witch resurrects skeletons against the backdrop of a burning ruined castle"
    discord = DiscordInteractions(
        token=discord_midjourney_payload["auth_token"],
        application_id=discord_midjourney_payload["application_id"],
        guild_id=discord_midjourney_payload["guild_id"],
        channel_id=discord_midjourney_payload["channel_id"],
        session_id=discord_midjourney_payload["session_id"],
        version=discord_midjourney_payload["version"],
        interaction_id=discord_midjourney_payload["interaction_id"],
    )
    response = await discord.post_interaction(my_text_prompt=prompt)
    print(response)
    bot = DiscordWatcher(watch_user_id=int(discord_midjourney_payload["application_id"]))
    bot.run(discord_watcher_token)


asyncio.run(main())
