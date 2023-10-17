# -*- coding: utf-8 -*-
"""
Filename: gpt_functions.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 15.10.2023
Last Modified: 17.10.2023

Description:
This file contains testing functions for ChatGPT function calling using DALLE and Leonardo experiments
"""
import json
from io import BytesIO

import requests
from PIL import Image

from examples.creds import oai_token, oai_organization
from leonardo_api.src.leonardo_api.leonardo_sync import Leonardo
from openai_api.src.openai_api.dalle import DALLE


def get_weather(city, units):
    """
    Get the weather for a given city.

    :param city: The city to get the weather for.
    :param units: The units to use for the weather.

    :return: The weather for the given city.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": "93171b03384f92ee3c55873452a49c7c", "units": units}
    response = requests.get(base_url, params=params)
    data = response.json()
    return data


def get_current_weather(location, unit="metric"):
    """
    Get the current weather in a given location

    :param location: (str) The location to get the weather for.
    :param unit: (str) The unit to use for the weather.
    """
    owm_info = get_weather(location, units=unit)
    weather_info = {
        "location": location,
        "temperature": owm_info["main"]["temp"],
        "unit": unit,
        "forecast": owm_info["weather"][0]["description"],
        "wind": owm_info["wind"]["speed"],
    }
    return json.dumps(weather_info)


def draw_image_using_dalle(prompt):
    """
    Draws image using user prompt. Returns url of image.

    :param prompt: (str) Prompt, the description, what should be drawn and how
    :return: (str) url of image
    """
    dalle = DALLE(auth_token=oai_token, organization=oai_organization)
    image = dalle.create_image_url(prompt)
    url_dict = {"image_url": image[0]}
    response = requests.get(image[0])
    img = Image.open(BytesIO(response.content))
    img.show()
    return json.dumps(url_dict)


def draw_image(prompt):
    """
    Draws image using user prompt. Returns url of image.

    :param prompt: (str) Prompt, the description, what should be drawn and how
    :return: (dict) dict with url of image
    """
    leonardo = Leonardo(auth_token="a0178171-c67f-4922-afb3-458f24ecef1a")
    leonardo.get_user_info()
    response = leonardo.post_generations(
        prompt=prompt,
        num_images=1,
        guidance_scale=5,
        model_id="e316348f-7773-490e-adcd-46757c738eb7",
        width=1024,
        height=768,
    )
    response = leonardo.wait_for_image_generation(generation_id=response["sdGenerationJob"]["generationId"])
    url_dict = {"image_url": response[0]["url"]}
    response = requests.get(url_dict["image_url"])
    img = Image.open(BytesIO(response.content))
    img.show()
    return json.dumps(url_dict)


gpt_functions = [
    {
        "name": "draw_image",
        "description": "Draws image using user prompt. Returns url of image.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Prompt, the description, what should be drawn and how",
                },
            },
            "required": ["prompt"],
        },
    },
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    },
]

gpt_functions_dict = {"get_current_weather": get_current_weather, "draw_image": draw_image}
