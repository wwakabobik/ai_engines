import asyncio

from openai_api.src.openai_api import DALLE
from creds import oai_token, oai_organization

from time import sleep

dalle = DALLE(auth_token=oai_token, organization=oai_organization)
async def main():
    resp = await dalle.create_image_url('robocop (robot policeman, from 80s movie)')
    print(resp)
    resp = await dalle.create_variation_from_url(resp[0])
    print(resp)

asyncio.run(main())