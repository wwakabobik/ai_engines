import requests
from PIL import Image
from io import BytesIO

import json

from creds import oai_token, oai_organization
from openai_api.src.openai_api.dalle import DALLE
from leonardo_api.leonardo_sync import Leonardo
from page_retriever import PageRetriever
from pytest_runner import run_tests


doc_engine = PageRetriever('https://wwakabobik.github.io/')


def get_weather(city, units):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": "93171b03384f92ee3c55873452a49c7c",
        "units": units
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data


def get_current_weather(location, unit="metric"):
    """Get the current weather in a given location"""
    owm_info = get_weather(location, units=unit)
    weather_info = {
        "location": location,
        "temperature": owm_info["main"]["temp"],
        "unit": unit,
        "forecast": owm_info["weather"][0]["description"],
        "wind": owm_info["wind"]["speed"]
    }
    return json.dumps(weather_info)


def draw_image_using_dalle(prompt):
    dalle = DALLE(auth_token=oai_token, organization=oai_organization)
    image = dalle.create_image_url(prompt)
    url_dict = {'image_url': image[0]}
    response = requests.get(image[0])
    img = Image.open(BytesIO(response.content))
    img.show()
    return json.dumps(url_dict)


def draw_image(prompt):
    leonardo = Leonardo(auth_token='a0178171-c67f-4922-afb3-458f24ecef1a')
    leonardo.get_user_info()
    response = leonardo.post_generations(prompt=prompt, num_images=1, guidance_scale=5,
                                         model_id='e316348f-7773-490e-adcd-46757c738eb7', width=1024, height=768)
    response = leonardo.wait_for_image_generation(generation_id=response['sdGenerationJob']['generationId'])
    url_dict = {'image_url': response[0]['url']}
    response = requests.get(url_dict['image_url'])
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
        {
            "name": "get_page_code",
            "description": "Get page code to generate locators and tests",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the page to get the code from"
                    }
                },
                "required": []
            }
        },
        {
            "name": "get_tests_results",
            "description": "Get the results of the tests",
            "parameters": {
                "type": "object",
                "properties": {
                    "test_files": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "The list of test files to run"
                    }
                },
                "required": []
            }
        }
    ]

gpt_functions_dict = {'get_current_weather': get_current_weather,
                      'draw_image': draw_image,
                      'get_page_code': doc_engine.get_body_without_scripts,
                      'get_tests_results': run_tests('tests/test_example.py')}