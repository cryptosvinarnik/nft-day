import aiohttp
import asyncio

from loguru import logger


async def subscribe_on_nft_day(worker: str, queue: asyncio.Queue) -> None:
    while not queue.empty():
        email = await queue.get()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://forms.hsforms.com/emailcheck/v1/json-ext",
                params={
                    'hs_static_app': 'forms-embed',
                    'hs_static_app_version': '1.2143',
                    'X-HubSpot-Static-App-Info': 'forms-embed-1.2143',
                    'portalId': '6444322',
                    'includeFreemailSuggestions': 'true',
                },
                data=email
            ) as resp:
                if (await resp.json()).get("success") is True:
                    logger.success(
                        f"{worker} - {email} successfully registered")
                else:
                    logger.error(f"{worker} - {email} - error!")


async def main(emails):
    queue = asyncio.Queue()

    for email in emails:
        queue.put_nowait(email)

    tasks = [asyncio.create_task(subscribe_on_nft_day(
             f"Worker {i}", queue)) for i in range(5)]

    await asyncio.gather(*tasks)
