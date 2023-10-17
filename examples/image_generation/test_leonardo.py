# -*- coding: utf-8 -*-
"""
Filename: test_leonardo.py
Author: Iliya Vereshchagin
Copyright (c) 2023. All rights reserved.

Created: 15.10.2023
Last Modified: 17.10.2023

Description:
This file contains testing procedures for Leonardo experiments
"""
import asyncio
import json

from leonardo_api import LeonardoAsync as Leonardo


async def main():
    """Main function"""
    leonardo = Leonardo(auth_token="a0178171-c67f-4922-afb3-458f24ecef1a")
    response = await leonardo.get_user_info()
    print(response)
    response = await leonardo.post_generations(
        prompt="a beautiful necromancer witch resurrects skeletons against " "the backdrop of a burning ruined castle",
        num_images=1,
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
