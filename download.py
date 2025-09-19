import aiohttp
import re
import logging
from urllib.parse import unquote

async def download_tiktok(url: str) -> bytes | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url + "/?lang=en") as resp:
                html = await resp.text()

        match = re.search(r'"playAddr":"(https:[^"]+)"', html)
        if not match:
            logging.error("Failed to find video URL in HTML")
            return None

        video_url = match.group(1)
        video_url = video_url.replace("\\u0026", "&")  
        video_url = video_url.replace("\\u002F", "/") 
        video_url = unquote(video_url)

        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as resp:
                if resp.status == 200:
                    logging.info(f"Video downloaded: {url}")
                    return await resp.read()
                else:
                    logging.error(f"Download status {resp.status}")
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
    return None
