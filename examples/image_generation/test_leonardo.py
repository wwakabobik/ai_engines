import json

import asyncio

from leonardo_api import LeonardoAsync as Leonardo


async def main():
    leonardo = Leonardo(auth_token='a0178171-c67f-4922-afb3-458f24ecef1a')
    response = await leonardo.get_user_info()
    print(response)
    response = await leonardo.post_generations(prompt="a beautiful necromancer witch resurrects skeletons against "
                                                      "the backdrop of a burning ruined castle", num_images=1,
                                               negative_prompt='bright colors, good characters, positive',
                                               model_id='e316348f-7773-490e-adcd-46757c738eb7', width=1024, height=768,
                                               guidance_scale=3)
    print(response)
    response = await leonardo.wait_for_image_generation(generation_id=response['sdGenerationJob']['generationId'])
    print(json.dumps(response[0]['url']))

asyncio.run(main())
