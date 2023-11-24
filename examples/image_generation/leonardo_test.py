# -*- coding: utf-8 -*-
"""
Filename: leonardo_test.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 15.10.2023
Last Modified: 20.11.2023

Description:
This file contains testing procedures for Leonardo experiments
"""

import json

import asyncio
from leonardo_api.leonardo_async import Leonardo

# pylint: disable=import-error
from examples.creds import leonardo_token  # type: ignore


async def main():
    """Main function"""
    leonardo = Leonardo(auth_token=leonardo_token)
    response = await leonardo.get_user_info()
    print(response)
    prompt = "a beautiful necromancer witch resurrects skeletons against the backdrop of a burning ruined castle"
    response = await leonardo.post_generations(
        prompt=prompt,
        num_images=2,
        negative_prompt="bright colors, good characters, positive",
        model_id="e316348f-7773-490e-adcd-46757c738eb7",
        width=1024,
        height=768,
        guidance_scale=3,
    )
    print(response)
    response = await leonardo.wait_for_image_generation(generation_id=response["sdGenerationJob"]["generationId"])
    print(json.dumps(response[0]["url"]))


asyncio.run(main())
