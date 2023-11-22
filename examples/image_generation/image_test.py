# -*- coding: utf-8 -*-
"""
Filename: image_test.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 21.11.2023
Last Modified: 21.11.2023

Description:
This file contains testing functions for image generation.
"""

import json
import re
import ssl
import time
from pprint import pprint

import aiofiles
import aiohttp
import asyncio
from ablt_python_api import ABLTApi_async as ABLTApi
from leonardo_api import LeonardoAsync as Leonardo
from openai_python_api.dalle import DALLE

from examples.creds import oai_token, oai_organization, leonardo_token, ablt_token, discord_midjourney_payload
from utils.discord_interactions import DiscordInteractions

# Initialize the APIs
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
dalle = DALLE(auth_token=oai_token, organization=oai_organization)
leonardo = Leonardo(auth_token=leonardo_token)
ablt = ABLTApi(bearer_token=ablt_token, ssl_context=ssl_context)


async def midjourney_wrapper(prompt):
    """
    Wrapper for midjourney testing.

    :param prompt: The prompt to use for the function.
    """
    discord = DiscordInteractions(
        token=discord_midjourney_payload["auth_token"],
        application_id=discord_midjourney_payload["application_id"],
        guild_id=discord_midjourney_payload["guild_id"],
        channel_id=discord_midjourney_payload["channel_id"],
        session_id=discord_midjourney_payload["session_id"],
        version=discord_midjourney_payload["version"],
        interaction_id=discord_midjourney_payload["interaction_id"],
    )
    await discord.post_interaction(my_text_prompt=prompt)
    return find_and_clear(log_file="discord_watcher.log")


async def leonardo_wrapper(prompt):
    response = await leonardo.post_generations(
        prompt=prompt,
        num_images=1,
        model_id="1e60896f-3c26-4296-8ecc-53e2afecc132",
        width=1024,
        height=1024,
        prompt_magic=True,
    )
    response = await leonardo.wait_for_image_generation(generation_id=response["sdGenerationJob"]["generationId"])
    return json.dumps(response["url"])


def find_and_clear(log_file):
    """
    Find and clear the log file.

    :param log_file: The log file to use for the function.
    :type log_file: str
    :return: The attachment found in the log file.
    :rtype: str
    """
    for _ in range(12):
        with open(log_file, "r+") as file:
            lines = file.readlines()
            for line in reversed(lines):
                match = re.search(r"Found an attachment: (.*)", line)
                if match:
                    file.truncate(0)
                    return match.group(1)
        time.sleep(5)
    return None


async def save_image_from_url(url, file_path):
    """
    Save image from url to file.

    :param url: The url to use for the function.
    :type url: str
    :param file_path: The file path to use for the function.
    :type file_path: str
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                f = await aiofiles.open(file_path, mode="wb")
                await f.write(await response.read())
                await f.close()
                print(f"Image successfully saved to {file_path}")
                return file_path
            print(f"Unable to save image. HTTP response code: {response.status}")
            return None


async def generate_image():
    prompts = (
        "beautiful and scary necromancer girl riding white unicorn",
        "draw a character that is a toast-mascot in cartoon style",
        "ai robots are fighting against humans in style of Pieter Bruegel",
    )
    image_list = []
    for index, prompt in enumerate(prompts):
        midjourney_prompt = await ablt.chat(
            bot_slug="maina",
            prompt=f"Please write a midjourney prompt with aspect ratio 1:1, realistic style: '{prompt}'. "
            f"Give me the prompt only, without any comments and descriptions. "
            f"Just prompt output for midjourney.",
            stream=False,
        ).__anext__()
        dalle_prompt = await ablt.chat(
            bot_slug="maina",
            prompt=f"Please write a dalle3 prompt: '{prompt}'. "
            f"Give me the prompt only, without any comments and descriptions. Just prompt output.",
            stream=False,
        ).__anext__()
        midjourney_prompt = midjourney_prompt.replace("`", "").replace("n", "")
        leonardo_image_url_coro = leonardo_wrapper(dalle_prompt)
        dalle3_image_url_coro = dalle.create_image_url(dalle_prompt)
        midjourney_image_url_coro = midjourney_wrapper(midjourney_prompt)
        leonardo_image_url, dalle3_image_url, midjourney_image_url = await asyncio.gather(
            leonardo_image_url_coro, dalle3_image_url_coro, midjourney_image_url_coro
        )
        leonardo_image_coro = save_image_from_url(leonardo_image_url[0], f"leonardo_image_{index}.png")
        dalle3_image_coro = save_image_from_url(dalle3_image_url[0], f"dalle3_image_{index}.png")
        midjourney_image_coro = save_image_from_url(midjourney_image_url, f"midjourney_image_{index}.png")
        leonardo_image, dalle3_image, midjourney_image = await asyncio.gather(
            leonardo_image_coro, dalle3_image_coro, midjourney_image_coro
        )
        image_list.append(
            {
                "images": {"leonardo": leonardo_image, "dalle3": dalle3_image, "midjourney": midjourney_image},
                "url": {"leonardo": leonardo_image_url, "dalle3": dalle3_image_url, "midjourney": midjourney_image_url},
            }
        )
    return image_list


async def get_dalle_variations(image_list):
    """
    Get variations from dalle3 images.

    :param image_list: The image list to use for the function.
    :type image_list: list
    :return: The variations from dalle3 images.
    :rtype: list
    """
    variations = []
    dalle.default_model = None  # disable dall-e-3 because isn't supported for variations yet
    for index, images in enumerate(image_list):
        file_path = images["images"]["dalle3"]
        # you may also use dalle.create_variation_from_url_and_get_url(url), but it's won't work for dalle3 urls
        with open(file_path, "rb") as file:
            url = await dalle.create_variation_from_file_and_get_url(file)
            image = await save_image_from_url(url, f"dalle3_variation_{index}.png")
            variations.append({"url": url, "image": image})
    return variations


async def main():
    """Main function."""
    image_list = await generate_image()
    pprint(image_list)
    dalle_variations = await get_dalle_variations(image_list)
    pprint(dalle_variations)


asyncio.run(main())
