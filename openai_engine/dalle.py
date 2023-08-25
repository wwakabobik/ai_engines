""" This module contains implementation for DALL-E """
# -*- coding: utf-8 -*-
import tempfile
import os
import uuid

import aiohttp
from io import BytesIO
import openai
from PIL import Image


class DALLE:
    def __init__(self, auth_token, organization, default_count=1, default_size="512x512", default_file_format='PNG',
                 user=None):
        self.___default_count = default_count
        self.___default_size = default_size
        self.___default_file_format = default_file_format
        self.___user = user
        self.___set_auth(auth_token, organization)

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

    async def create_image(self, prompt):
        """
        Creates an image using DALL-E Image API.

        :param prompt: The prompt to be used for image creation.

        :return: A PIL.Image object created from the image data received from the API.
        """
        response = await openai.Image.acreate(prompt=prompt, n=self.default_count, size=self.default_size,
                                              user=self.user)
        image_url = response["data"][0]["url"]
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                image_data = await resp.read()
        return Image.open(BytesIO(image_data))

    @staticmethod
    def show_image(image):
        """
        Shows image interactively.

        :param image: image object.
        """
        image.show()

    def save_image(self, image, filename=None, file_format=None):
        """ Saves an image to a file.

        :param image: A PIL.Image object to be saved.
        :param filename: The name of the file where the image will be saved.
                         If None, a random filename in the system's temporary directory will be used.
        :param file_format: The format of the file. This is optional and defaults to 'PNG'.

        :return: The full path of the file where the image was saved, or None if the image could not be saved.
        """
        if file_format is None:
            file_format = self.default_file_format
        if filename is None:
            filename = os.path.join(tempfile.gettempdir(), f'{uuid.uuid4()}.{file_format.lower()}')
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
        response = await openai.Image.acreate_variation(file=file, n=self.default_count, size=self.default_size,
                                                        user=self.user)
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

        response = await openai.Image.acreate_variation(BytesIO(image_data), n=self.default_count,
                                                        size=self.default_size,
                                                        user=self.user)
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
        response = await openai.Image.acreate_edit(file=file, prompt=prompt, mask=mask,
                                                   n=self.default_count, size=self.default_size,
                                                   user=self.user)
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
        response = await openai.Image.acreate_edit(file=BytesIO(image_data), prompt=prompt, mask=BytesIO(mask_data),
                                                   n=self.default_count, size=self.default_size,
                                                   user=self.user)
        image_url = response["data"][0]["url"]
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                image_data = await resp.read()
        return Image.open(BytesIO(image_data))
