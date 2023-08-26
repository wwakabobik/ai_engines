# -*- coding: utf-8 -*-
"""
Filename: dalle.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 25.08.2023
Last Modified: 26.08.2023

Description:
This file contains implementation for DALL-E
"""
import logging
import os
import tempfile
import uuid
from io import BytesIO

import aiohttp
import asyncio
import openai
from PIL import Image


class DALLE:
    """
    The ChatGPT class is for managing an instance of the ChatGPT model.

    Parameters:
    auth_token (str): Authentication bearer token. Required.
    organization (str): Organization uses auth toke. Required.
    default_count (int): Default count of images to produce. Default is 1.
    default_size (str): Default dimensions for output images. Default is "512x512". "256x256" and "1024x1024" as option.
    default_file_format (str): Default file format. Optional. Default is 'PNG'.
    user (str, optional): The user ID. Default is ''.
    logger (logging.Logger, optional): default logger. Default is None.
    """

    def __init__(
        self,
        auth_token: str,
        organization: str,
        default_count: int = 1,
        default_size: str = "512x512",
        default_file_format: str = "PNG",
        user: str = "",
        logger: logging.Logger = None,
    ):
        """
        General init

        :param auth_token (str): Authentication bearer token. Required.
        :param organization (str): Organization uses auth toke. Required.
        :param default_count:  Default count of images to produce. Optional. Default is 1.
        :param default_size:  Default dimensions for output images. Optional. Default is "512x512".
        :param default_file_format:  Default file format. Optional. Optional. Default is 'PNG'.
        :param user: The user ID. Optional. Default is ''.
        :param logger: default logger. Optional. Default is None.
        """
        self.___default_count = default_count
        self.___default_size = default_size
        self.___default_file_format = default_file_format
        self.___user = user
        self.___set_auth(auth_token, organization)
        self.___logger = logger

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
    def default_count(self):
        """
        Getter for default_count.

        :return: Returns default_count value.
        """
        return self.___default_count

    @default_count.setter
    def default_count(self, value):
        """
        Setter for default_count.

        :param value: The new value of default_count.
        """
        self.___default_count = value

    @property
    def default_size(self):
        """
        Getter for default_size.

        :return: Returns default_size value.
        """
        return self.___default_size

    @default_size.setter
    def default_size(self, value):
        """
        Setter for default_size.

        :param value: The new value of  default_size.
        """
        self.___default_size = value

    @property
    def default_file_format(self):
        """
        Getter for default_file_format.

        :return: Returns default_file_format value.
        """
        return self.___default_file_format

    @default_file_format.setter
    def default_file_format(self, value):
        """
        Setter for default_size.

        :param value: The new value of default_file_format.
        """
        self.___default_file_format = value

    @property
    def user(self):
        """
        Getter for user.

        :return: The user.
        """
        return self.___user

    @user.setter
    def user(self, value):
        """
        Setter for user.

        :param value: The user.
        """
        self.___user = value

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

    async def create_image(self, prompt):
        """
        Creates an image using DALL-E Image API.

        :param prompt: The prompt to be used for image creation.

        :return: A PIL.Image object created from the image data received from the API.
        """
        response = await openai.Image.acreate(
            prompt=prompt, n=self.default_count, size=self.default_size, user=self.user
        )
        return response["data"]

    def screate_image(self, prompt):  # FIXME let it be till experiment, then remove
        """
        Creates an image using DALL-E Image API.

        :param prompt: The prompt to be used for image creation.

        :return: A PIL.Image object created from the image data received from the API.
        """
        response = openai.Image.create(
            prompt=prompt, n=self.default_count, size=self.default_size, user=self.user
        )
        return response["data"]

    async def create_image_url(self, prompt):
        """
        Creates an image using DALL-E Image API, returns list of URLs with images.

        :param prompt: The prompt to be used for image creation.

        :return: list of URLs
        """
        image_urls = list()
        for items in await self.create_image(prompt):
            image_urls.append(items['url'])
        return image_urls

    def screate_image_url(self, prompt):  # FIXME let it be till experiment, then remove
        """
        Creates an image using DALL-E Image API, returns list of URLs with images. (SYNC)

        :param prompt: The prompt to be used for image creation.

        :return: list of URLs
        """
        image_urls = list()
        for items in self.screate_image(prompt):
            image_urls.append(items['url'])
        return image_urls

    @staticmethod
    async def convert_image_from_url_to_bytes(url):
        """
        Converts image from URL to bytes format.

        :param url: URL of image.

        :return: URL
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                image_data = await resp.read()
        return Image.open(BytesIO(image_data))

    async def create_image_data(self, prompt):
        """
        Creates an image using DALL-E Image API, returns list of images (bytes format).

        :param prompt: The prompt to be used for image creation.

        :return: list of images (bytes format).
        """
        tasks = []
        async for items in await self.create_image(prompt):
            task = asyncio.ensure_future(self.convert_image_from_url_to_bytes(items['url']))
            tasks.append(task)
        image_data = await asyncio.gather(*tasks)
        return image_data

    @staticmethod
    def show_image(image):
        """
        Shows image interactively.

        :param image: image object.
        """
        image.show()

    def save_image(self, image, filename=None, file_format=None):
        """Saves an image to a file.

        :param image: A PIL.Image object to be saved.
        :param filename: The name of the file where the image will be saved.
                         If None, a random filename in the system's temporary directory will be used.
        :param file_format: The format of the file. This is optional and defaults to 'PNG'.

        :return: The full path of the file where the image was saved, or None if the image could not be saved.
        """
        if file_format is None:
            file_format = self.default_file_format
        if filename is None:
            filename = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.{file_format.lower()}")
        try:
            image.save(filename, format=format)
        except Exception as error:
            print(f"Can't save image: {error}")
            return None
        return filename

    async def create_variation_from_file(self, file):
        """
        Creates an image variation from file using DALL-E Image API.

        :param file: file of the image (bytes).

        :return: A PIL.Image object created from the image data received from the API.
        """
        response = await openai.Image.acreate_variation(
            image=file, n=self.default_count, size=self.default_size, user=self.user
        )
        image_url = response["data"][0]["url"]
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                image_data = await resp.read()
        return Image.open(BytesIO(image_data))

    async def create_variation_from_url(self, url):
        """
        Creates an image variation from URL using DALL-E Image API.

        :param url: URL of the image.

        :return: A PIL.Image object created from the image data received from the API.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                image_data = await resp.read()

        response = await openai.Image.acreate_variation(
            image=BytesIO(image_data), n=self.default_count, size=self.default_size, user=self.user
        )
        image_url = response["data"][0]["url"]
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                variation_image_data = await resp.read()
        return Image.open(BytesIO(variation_image_data))

    async def edit_image_from_file(self, file, prompt, mask=None):
        """
        Edits an image using OpenAI's Image API.

        :param file: A file-like object opened in binary mode containing the image to be edited.
        :param prompt: The prompt to be used for image editing.
        :param mask: An optional file-like object opened in binary mode containing the mask image.
                     If provided, the mask will be applied to the image.
        :return: A PIL.Image object created from the image data received from the API.
        """
        response = await openai.Image.acreate_edit(
            image=file, prompt=prompt, mask=mask, n=self.default_count, size=self.default_size, user=self.user
        )
        image_url = response["data"][0]["url"]
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                image_data = await resp.read()
        return Image.open(BytesIO(image_data))

    async def edit_image_from_url(self, url, prompt, mask_url=None):
        """
        Edits an image using OpenAI's Image API.

        :param url: A url of image to be edited.
        :param prompt: The prompt to be used for image editing.
        :param mask_url: Url containing mask image. If provided, the mask will be applied to the image.
        :return: A PIL.Image object created from the image data received from the API.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                image_data = await resp.read()

        async with aiohttp.ClientSession() as session:
            async with session.get(mask_url) as resp:
                mask_data = await resp.read()
        response = await openai.Image.acreate_edit(
            image=BytesIO(image_data),
            prompt=prompt,
            mask=BytesIO(mask_data),
            n=self.default_count,
            size=self.default_size,
            user=self.user,
        )
        image_url = response["data"][0]["url"]
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                image_data = await resp.read()
        return Image.open(BytesIO(image_data))
